from collections import Counter
import math
import random
import numpy as np
from scipy.stats import chi2, norm
import matplotlib.pyplot as plt

# -------------- Generadores de números aleatorios --------------
# ------ Test 1. Metodo de los Cuadrados
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
# normalización de los resultados a (0,1)
u_mid_square = [v / (10 ** len(str(abs(v))))  for _, v in resultado_mid_square]

#mostramos resultados
# print("METODO DE LOS CUADRADOS")
# print(f"{'Nueva Semilla':<15} | {'Valor (Cuadrado)':<15} | {'Normalizado (0,1)'}")
# print("-" * 60)
# for i, (s, v) in enumerate(resultado_mid_square, start=1):
#     seed_str = f"{s:04d}"
#     u = u_mid_square[i - 1]
#     print(f"{i:03d} | {seed_str:<15} | {v:<15} | {u:.10f}")



# ------ Test 2. Congruencia Lineal
def linear_congruential_generator(seed, a, c, m, n):
    values = []
    for _ in range(n):
        seed = (a * seed + c) % m
        values.append(seed)
    return values

# ejecución del ejemplo
resultado_linear_congruential_generator = linear_congruential_generator(1, 1664525, 1013904223, 2**32, 10)
# normalización de los resultados a (0,1)
u_rand_linear = [x / (10 ** len(str(abs(x)))) for x in resultado_linear_congruential_generator]

#mostrar resultados
# print(f"METODO DE CONGRUENCIA LINEAL")
# for i in range(len(resultado_linear_congruential_generator)):
#    print(f"{i+1:03d} | {resultado_linear_congruential_generator[i]:010d}")
#normalizacion de los resultados a (0,1)
# for i in range(len(u_rand_linear)):
#    print(f"{i+1:03d} | {u_rand_linear[i]:.10f}")

# ------ Test 3. 1000 numeros generados con random() de Python
u_rand_python = [random.random() for _ in range(1000)]




# -------------------------- TESTS --------------------------
def test_esperas(u_rand, b_inicio, b_fin, alpha = 0.05):
    p_intervalo = b_fin - b_inicio # probabilidad de caer en el intervalo (b_inicio, b_fin)
    n = len(u_rand)

    hits = [i for i, x in enumerate(u_rand, start=1) if b_inicio < x < b_fin]
    if len(hits) < 2:
        return {"chi2": 0.0, "p_value": 1.0, "decision": "No datos suficientes"}
    
    # Calcular los "tiempos de espera" (brecha entre ocurrencias)
    esperas = []
    last_pos = 0
    for pos in hits:
        esperas.append(pos - last_pos)
        last_pos = pos
    # Calcular frecuencias y prueba Chi Cuadrado
    frec_obs = Counter(esperas)
    max_espera = max(esperas)

    x2 = 0.0
    total_esperas = len(esperas)

    for k in range(1, max_espera + 1):
        obs = frec_obs.get(k, 0)
        # Probabilidad geométrica: P(X=k) = p * (1-p)^(k-1)
        prob_geom = p_intervalo * ((1 - p_intervalo) ** (k - 1))
        # Frecuencia esperada respecto a los N intentos:
        geom_esperado = total_esperas * prob_geom
        if geom_esperado > 0:
            x2 += ((obs - geom_esperado) ** 2) / geom_esperado   
    grados_libertad = max_espera - 1
    p_value = chi2.sf(x2, grados_libertad) if grados_libertad > 0 else 1.0
    
    pasa = p_value > alpha

    print(f"p-value: {p_value:.4f}, alpha: {alpha}, Pasa: {'Sí' if pasa else 'No'}")

def frecuencia_monobit(valores, alpha=0.05):
    bits = [1 if u >= 0.5 else 0 for u in valores]
    bits = np.array(bits)
    n = len(bits)

    x = 2*bits - 1  # Convertir 0 a -1 y 1 a +1
    suma = np.sum(x)
    z = abs(suma) / np.sqrt(n)
    z_crit = norm.ppf(1 - alpha/2)

    pasa = z < z_crit
    print(f"Z: {z:.4f}, Z Critico: {z_crit:.4f}, Pasa: {'Sí' if pasa else 'No'}")

def runs_test(valores, alpha=0.05):
    promedio = np.median(valores)

    # convertir a A/B
    seq = ['1' if x >= promedio else '2' for x in valores]
    # contar rachas
    runs = 1
    for i in range(1, len(seq)):
        if seq[i] != seq[i-1]:
            runs += 1
    n1 = seq.count('1')
    n2 = seq.count('2')

    # promedio
    prom = (2*n1*n2)/(n1+n2) + 1
    # varianza
    var = (2*n1*n2*(2*n1*n2 - n1 - n2)) / \
          (((n1+n2)**2)*(n1+n2-1))
    Z = (runs - prom) / np.sqrt(var)
    z_crit = norm.ppf(1 - alpha/2)

    pasa = abs(Z) < z_crit
    print(f"Z: {Z:.4f}, Z Critico: {z_crit:.4f}, Pasa: {'Sí' if pasa else 'No'}")

def bondad_ajuste_chi_cuadrado(valores, cant_celdas=10, alpha=0.05):
    n = len(valores)
    frecuencia_esperada = n / cant_celdas
    intervalos = np.linspace(0, 1, cant_celdas + 1) # Dividir el rango (0,1) en 'cant_celdas' intervalos iguales
    grados_libertad = cant_celdas - 1 # Grados de libertad para la prueba chi-cuadrado

    frecuencias_observadas, _ = np.histogram(valores, intervalos) # Contar cuántos valores caen en cada intervalo
    # Estadístico calculado
    chi_calculado = np.sum(
        ((frecuencias_observadas - frecuencia_esperada) ** 2)
        / frecuencia_esperada
    )
    # Valor crítico
    chi_critico = chi2.ppf(1 - alpha, grados_libertad)

    pasa = chi_calculado < chi_critico

    print(f"Chi Calculado: {chi_calculado:.4f}, Chi Crítico: {chi_critico:.4f}, Pasa: {'Sí' if pasa else 'No'}") 

print("\nResultado para Python random():")
print("-------------------------------------------")
print(f"1. Test de Esperas:")
test_esperas(u_rand_python, 0.3, 0.6)
print(f"2. Monobit Test:")
frecuencia_monobit(u_rand_python)
print(f"3. Runs Test:")
runs_test(u_rand_python)
print(f"4. Test Chi-Cuadrado:")
bondad_ajuste_chi_cuadrado(u_rand_python)

print("\nResultado para Congruencia Lineal:")
print("-------------------------------------------")
print(f"1. Test de Esperas:")
test_esperas(u_rand_linear, 0.3, 0.6)
print(f"2. Monobit Test:")
frecuencia_monobit(u_rand_linear)
print(f"3. Runs Test:")
runs_test(u_rand_linear)
print(f"4. Test Chi-Cuadrado:")
bondad_ajuste_chi_cuadrado(u_rand_linear)

print("\nResultado para Método de los Cuadrados:")
print("-------------------------------------------")
print(f"1. Test de Esperas:")
test_esperas(u_mid_square, 0.3, 0.6)
print(f"2. Monobit Test:")
frecuencia_monobit(u_mid_square)
print(f"3. Runs Test:")
runs_test(u_mid_square)
print(f"4. Chi-Squared Test:")
bondad_ajuste_chi_cuadrado(u_mid_square)


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


