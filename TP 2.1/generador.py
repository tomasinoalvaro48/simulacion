from collections import Counter
import math
import random
import numpy as np
from scipy.stats import chi2
import matplotlib.pyplot as plt

# -------------- Generadores de números aleatorios --------------
# Test 1. Metodo de los Cuadrados
def mid_square(seed, n):
    seeds = []
    values = []
    # Un bucle que se repite 'n' veces
    for _ in range(n):
        x = seed ** 2  
        # Convertimos 'x' a string de texto para contar sus caracteres
        if len(str(x)) > 2:
            # // es la división entera y % es el módulo
            seed = (x // 10**2) % 10**4
        else:
            seed = 0
        values.append(x)
        seeds.append(seed)
    return list(zip(seeds, values))

# ejecución de ejemplo
resultado_mid_square = mid_square(9731, 100)
#normalización de los resultados a (0,1)
u_mid_square = [v / (10 ** len(str(abs(v))))  for _, v in resultado_mid_square]
#mostramos resultados
print("METODO DE LOS CUADRADOS")
print(f"{'Nueva Semilla':<15} | {'Valor (Cuadrado)'}")
print("-" * 35)
i=0
for s, v in resultado_mid_square:
    i += 1
    seed_str = f"{s:04d}"
    print(f"{i:03d} | {seed_str:<15} | {v}")



# Test 2. Congruencia Lineal
'''
Los Generadores Congruenciales Lineales (GCL) tienen la forma
x_{n+1} = (a * x_n + c) mod m
Donde
- a es la multiplicadora
- c es la incrementadora
- m es el módulo
- x_0 es la semilla inicial
'''
def linear_congruential_generator(seed, a, c, m, n):
    values = []
    for _ in range(n):
        seed = (a * seed + c) % m
        values.append(seed)
    return values

# ejecución del ejemplo
resultado_linear_congruential_generator = linear_congruential_generator(1, 1664525, 1013904223, 2**32, 10)
print(f"METODO DE CONGRUENCIA LINEAL")
#mostrar resultados
for i in range(len(resultado_linear_congruential_generator)):
    print(f"{i+1:03d} | {resultado_linear_congruential_generator[i]:010d}")
#normalizacion de los resultados a (0,1)
u_rand_linear = [x / (10 ** len(str(abs(x)))) for x in resultado_linear_congruential_generator]
for i in range(len(u_rand_linear)):
    print(f"{i+1:03d} | {u_rand_linear[i]:.10f}")






# ------------ TESTS --------------
'''
H 0 : independencia y uniformidad
Procedimiento:
1. Seleccionar un subintervalo del (0 , 1).
2. Calcular la probabilidad del subintervalo.
3. Ubicar en la sucesión las posiciones de los elementos que pertenezcan al subintervalo.
4. Calcular el número de elementos consecutivos de la sucesión entre cada una de las ocurrencias consecutivas de elementos del subintervalo (tiempos de espera).
5. La distribución de los tiempos de espera es geométrica con parámetro calculado en 2.
6. Aplicar una prueba  χ ^ 2 a los tiempos de espera.
'''

def test_esperas(u_rand, b_inicio, b_fin):
    p_intervalo = b_fin - b_inicio
    # 3. Ubicar posiciones de los elementos en el intervalo (1-based index)
    posiciones_hits = [i for i, x in enumerate(u_rand, start=1) if b_inicio < x < b_fin]
    if not posiciones_hits:
        return {"x2": 0.0, "p_value": 0.0}
    # 4. Calcular los "tiempos de espera" (brecha entre ocurrencias)
    esperas = []
    last_pos = 0
    for pos in posiciones_hits:
        esperas.append(pos - last_pos)
        last_pos = pos
    # 5. y 6. Calcular frecuencias y prueba Chi Cuadrado
    frec_obs = Counter(esperas)
    max_espera = max(esperas)
    x2 = 0.0
    for k in range(1, max_espera + 1):
        obs = frec_obs.get(k, 0)
        # Probabilidad geométrica: P(X=k) = p * (1-p)^(k-1)
        prob_geom = p_intervalo * ((1 - p_intervalo) ** (k - 1))
        # Frecuencia esperada respecto a los N intentos:
        geom_esperado = len(u_rand) * prob_geom
        if geom_esperado > 0:
            x2 += ((obs - geom_esperado) ** 2) / geom_esperado   
    df = max_espera - 1
    p_value = 1.0 - chi2.cdf(x2, df=df) if df > 0 else 1.0
    return {"x2": float(x2), "p_value": float(p_value)}

def frecuencia_monobit(values):
    # Accepts 0/1 or general integers (uses LSB as the bit).
    normalized_bits = []
    bits = [1 if u >= 0.5 else 0 for u in values]
    for b in bits:
        if b in (0, 1):
            normalized_bits.append(int(b))
        else:
            normalized_bits.append(int(b) & 1)
    data = "".join(str(b) for b in normalized_bits)
    if len(data) == 0:
        return {"p_value": 1.0, "pass": True}
    mm_unos = [(2 * int(bit)) - 1 for bit in data]
    suma = sum(mm_unos)
    suma_abs = abs(suma) / math.sqrt(len(data))
    p_value = math.erfc(suma_abs / math.sqrt(2))
    return {"p_value": p_value, "pass": p_value > 0.01}

def runs_test(values, median=None):
    data = np.asarray(values)
    if data.size == 0:
        return {"z": 0.0, "runs": 0, "n1": 0, "n2": 0}
    if median is None:
        median = float(np.median(data))
    above = data >= median
    n1 = int(np.sum(above))
    n2 = int(data.size - n1)
    runs = 1
    for i in range(1, data.size):
        if above[i] != above[i - 1]:
            runs += 1
    runs_exp = (2 * n1 * n2) / (n1 + n2) + 1
    stan_dev = math.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) /
                         (((n1 + n2) ** 2) * (n1 + n2 - 1)))
    z = (runs - runs_exp) / stan_dev if stan_dev != 0 else 0.0
    return {"z": z, "runs": runs, "n1": n1, "n2": n2}

def bondad_ajuste_chi_cuadrado(o_i, bins=10):
    # Accepts either class labels 1..bins or raw values in [0, 1).
    values = []
    for item in o_i:
        if isinstance(item, tuple) and len(item) >= 2:
            values.append(item[1])
        else:
            values.append(item)
    is_class_labels = all(isinstance(v, (int, np.integer)) and 1 <= v <= bins for v in values)
    if is_class_labels:
        classes = values
    else:
        classes = [min(int(float(v) * bins), bins - 1) + 1 for v in values]
    expected = np.full(bins, len(classes) / bins)
    observed = Counter(classes)
    observed_counts = np.array([observed.get(i, 0) for i in range(1, bins + 1)])
    x2 = np.sum((observed_counts - expected) ** 2 / expected)
    p_value = 1.0 - chi2.cdf(x2, df=bins - 1)
    return {"x2": float(x2), "p_value": float(p_value)}

print("Resultado para Congruencia Lineal:")
print("-----------------------------")
print(f"Test de Esperas: {test_esperas(u_rand_linear, 0.5, 1.0)}")
print(f"Monobit Test: {frecuencia_monobit(u_rand_linear)}")
print(f"Runs Test: {runs_test(u_rand_linear)}")
print(f"Test Chi-Cuadrado: {bondad_ajuste_chi_cuadrado(resultado_linear_congruential_generator)}")

print("\nResultado para Método de los Cuadrados:")
print("-----------------------------")
print(f"Test de Esperas: {test_esperas(u_mid_square, 0.5, 1.0)}")
print(f"Monobit Test: {frecuencia_monobit(u_mid_square)}")
print(f"Runs Test: {runs_test(u_mid_square)}")
print(f"Chi-Squared Test: {bondad_ajuste_chi_cuadrado(resultado_mid_square)}")


# ------------ GRAFICOS (MAPAS DE BITS) --------------
def graficar_mapas_de_bits_comparacion():
    # Generar 40,000 números para armar una cuadrícula de 200x200 pixeles
    n_puntos = 40000
    dimension = 200
    
    # 1. Usar GCL definido arriba (parámetros buenos predeterminados)
    gcl_bueno = linear_congruential_generator(12345, 1664525, 1013904223, 2**32, n_puntos)
    u_gcl_bueno = [x / (2**32) for x in gcl_bueno]
    
    # 2. Generador deliberadamente "malo" (para notar visualmente los patrones, análogo a rand viejos)
    # Usamos parámetros con un módulo pequeño y multiplicadores inadecuados
    gcl_malo = linear_congruential_generator(12345, 106, 1283, 6075, n_puntos)
    u_gcl_malo = [x / 6075 for x in gcl_malo]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Convertir a 0 (negro) o 1 (blanco) usando el umbral de 0.5
    grid_bueno = np.where(np.array(u_gcl_bueno) >= 0.5, 1, 0).reshape((dimension, dimension))
    grid_malo = np.where(np.array(u_gcl_malo) >= 0.5, 1, 0).reshape((dimension, dimension))

    ax1.imshow(grid_bueno, cmap='gray', interpolation='nearest')
    ax1.set_title("GCL: Parámetros Buenos\n(Ruido uniforme)")
    ax1.axis('off')

    ax2.imshow(grid_malo, cmap='gray', interpolation='nearest')
    ax2.set_title("GCL: Parámetros Malos\n(Patrones/franjas visibles)")
    ax2.axis('off')

    plt.tight_layout()
    plt.show()

def graficar_mapas_de_bits_bueno_malo():
    # Generar 40,000 números para armar una cuadrícula de 200x200 pixeles
    n_puntos = 40000
    dimension = 200
    semilla = 9731  # Usar la misma semilla para los dos
    
    # 1. Metodo de los cuadrados
    resultado_cuadrados = mid_square(semilla, n_puntos)
    # Normalizamos dividiendo por 10^8 (ya que el cuadrado máximo de una semilla de 4 digitos es ~99980001)
    u_cuadrados = [v / (10**8) for _, v in resultado_cuadrados]
    
    # 2. Generador Congruencial Lineal
    gcl = linear_congruential_generator(semilla, 1664525, 1013904223, 2**32, n_puntos)
    u_gcl = [x / (2**32) for x in gcl]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Convertir a 0 (negro) o 1 (blanco) usando el umbral de 0.5
    grid_cuadrados = np.where(np.array(u_cuadrados) >= 0.5, 1, 0).reshape((dimension, dimension))
    grid_gcl = np.where(np.array(u_gcl) >= 0.5, 1, 0).reshape((dimension, dimension))

    ax1.imshow(grid_cuadrados, cmap='gray', interpolation='nearest')
    ax1.set_title("Método de los Cuadrados\n(Rápida degeneración a 0)")
    ax1.axis('off')

    ax2.imshow(grid_gcl, cmap='gray', interpolation='nearest')
    ax2.set_title("Congruencia Lineal (GCL)\n(Ruido uniforme)")
    ax2.axis('off')

    plt.tight_layout()
    plt.show()

def graficar_mapas_de_bits_comparacion_generadores():
    # Generar 40,000 numeros para armar una cuadricula de 200x200 pixeles
    n_puntos = 40000
    dimension = 200
    semilla = 9731

    # 1. Metodo de los cuadrados
    resultado_cuadrados = mid_square(semilla, n_puntos)
    u_cuadrados = [v / (10**8) for _, v in resultado_cuadrados]

    # 2. Generador Congruencial Lineal
    gcl = linear_congruential_generator(semilla, 1664525, 1013904223, 2**32, n_puntos)
    u_gcl = [x / (2**32) for x in gcl]

    # 3. Generador de Python (random)
    rng = random.Random(semilla)
    u_python = [rng.random() for _ in range(n_puntos)]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    grid_cuadrados = np.where(np.array(u_cuadrados) >= 0.5, 1, 0).reshape((dimension, dimension))
    grid_gcl = np.where(np.array(u_gcl) >= 0.5, 1, 0).reshape((dimension, dimension))
    grid_python = np.where(np.array(u_python) >= 0.5, 1, 0).reshape((dimension, dimension))

    ax1.imshow(grid_cuadrados, cmap='gray', interpolation='nearest')
    ax1.set_title("Metodo de los Cuadrados\n(Rapida degeneracion a 0)")
    ax1.axis('off')

    ax2.imshow(grid_gcl, cmap='gray', interpolation='nearest')
    ax2.set_title("Congruencia Lineal (GCL)\n(Ruido uniforme)")
    ax2.axis('off')

    ax3.imshow(grid_python, cmap='gray', interpolation='nearest')
    ax3.set_title("Python random\n(MT19937)")
    ax3.axis('off')

    plt.tight_layout()
    plt.show()

graficar_mapas_de_bits_bueno_malo()

graficar_mapas_de_bits_comparacion()

graficar_mapas_de_bits_comparacion_generadores()


