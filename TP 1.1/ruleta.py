import numpy as np # pip install matplotlib: libreria con numpy y pyplot
import matplotlib.pyplot as plt
import argparse


# --------------- Manejo de argumentos de linea de comandos al ejecutar el script ---------------
# python ruleta.py -n XXX -c YYY -e ZZ
parser = argparse.ArgumentParser(description='Simulación de Ruleta.')
parser.add_argument('-n', '--muestras', type=int, required=True, help='Cantidad de muestras por corrida')
parser.add_argument('-c', '--corridas', type=int, required=True, help='Cantidad de corridas/simulaciones')
parser.add_argument('-e', '--elegido', type=int, required=True, help='Número apostado/elegido')

# ----------- Definicion de constantes y variables -----------
# Caracteristicas de la simulacion
args = parser.parse_args()
tiradas = args.muestras
corridas = args.corridas
numero_elegido = args.elegido

# Caracteristicas de la ruleta
cant_numeros_ruleta = 37 # Números del 0 al 36
valores_ruleta = np.arange(cant_numeros_ruleta) # Array con los valores 0 a 36 de la ruleta

# --------- Datos Esperados ---------
# Distribucion Uniforme Discreta
fa_e = tiradas / cant_numeros_ruleta # Frecuencia absoluta esperada
fr_e = 1.0 / cant_numeros_ruleta # Frecuencia relativa esperada
vp_e = valores_ruleta.sum() / cant_numeros_ruleta  # Valor promedio esperado
desv_e = float(np.std(valores_ruleta)) # Desvio estandar esperado
vari_e = float(np.var(valores_ruleta)) # Varianza esperada

# ----------- Inicio de la simulación -----------
print(f"Simulando {corridas} corridas de {tiradas} tiradas. Apostando al {numero_elegido}...")
print("")

fa = [] # Frecuencia absoluta de cada numero por corrida. fa[i][j] = corrida i, numero j
fr_a = [] # Frecuencia relativa de cada numero acumulada por corrida. fr_a[i][j][k] = corrida i, numero j, tirada k
vp_a = [] # Valor promedio acumulado por corrida. vp_a[i][k] = corrida i, tirada k
vd_a = [] # Valor desvio acumulado por corrida. vd_a[i][k] = corrida i, tirada k
vv_a = [] # Valor varianza acumulado por corrida. vv_a[i][k] = corrida i, tirada k

for corrida in range(corridas):
    valores = np.random.randint(0, cant_numeros_ruleta, tiradas)

    prueba = []
    # Frecuencia absoluta por numero
    fa_c = []
    for numero in range(cant_numeros_ruleta):
        fa_c.append(int(np.sum(valores == numero))) # Cuenta cuántas veces aparece el número en las muestras de la corrida
    fa.append(fa_c)


    # Frecuencia relativa acumulada por numero
    fr_a_c = []
    muestras = np.arange(1, tiradas + 1)
    for numero in range(cant_numeros_ruleta):
        acumulado_numero = np.cumsum(valores == numero) # Suma acumulada de cuántas veces apareció el número en las muestras de la corrida
        fr_a_c.append((acumulado_numero / muestras).astype(float).tolist()) # Frecuencia relativa acumulada por numero y corrida
    fr_a.append(fr_a_c)

    # Promedio acumulado
    acumulado = np.cumsum(valores) # Suma acumulada de los valores de las muestras de la corrida
    vp_c = (acumulado / muestras).astype(float)
    vp_a.append(vp_c.tolist())

    # Varianza acumulada
    acumulado_sq = np.cumsum(valores ** 2)
    vv_c = ((acumulado_sq / muestras) - (vp_c ** 2))
    vv_a.append(vv_c.astype(float).tolist())

    # Desvio acumulado
    vd_c = np.sqrt(vv_c)
    vd_a.append(vd_c.astype(float).tolist())












#----------------------------------------------------
#---------------- GRAFICOS 1 CORRIDA ----------------

# --------- Graficos de comparación en UNA corrida ---------
# Grafico 1: Gráfico de bastones - Frecuencia Absoluta
plt.stem(range(cant_numeros_ruleta), fa[0], label='Frecuencia Absoluta')
plt.axhline(y=fa_e, color='r', linestyle='--', label='Frecuencia Absoluta Esperada')
plt.title("Gráfico de Bastones - Frecuencia Absoluta de cada número en una corrida")
plt.xlabel("Valores de la Ruleta")
plt.ylabel("Cantidad de veces que salió")
plt.legend() 
plt.show()

# Grafico 2
# Dibuja el gráfico de valor promedio acumulado para el nro elegido a lo largo de las tiradas de una corrida
plt.plot(range(1, tiradas+1), vp_a[0], label='Valor Promedio de una corrida')
plt.axhline(y=vp_e, color='r', linestyle='--', label='Valor Promedio Esperado') 
plt.title("Número de Tiradas sobre Valor Promedio acumulado en una corrida") 
plt.xlabel("Número de tiradas") 
plt.ylabel("Valor Promedio") 
plt.legend() 
plt.show()

# Grafico 3
# Dibuja el gráfico de valor desvio acumulado para el nro elegido a lo largo de las tiradas de una corrida
plt.plot(range(1, tiradas+1), vd_a[0], label=f'Valor Desvio del número {numero_elegido}')
plt.axhline(y=desv_e, color='r', linestyle='--', label='Valor Desvio Esperado')
plt.title("Número de Tiradas sobre Valor Desvio acumulado en una corrida")
plt.xlabel("Número de tiradas")
plt.ylabel("Valor Desvio") 
plt.legend()
plt.show()

# Grafico 4
# Dibuja el gráfico de valor varianza acumulado para el nro elegido a lo largo de las tiradas de una corrida
plt.plot(range(1, tiradas+1), vv_a[0], label=f'Valor Varianza del número {numero_elegido}')
plt.axhline(y=vari_e, color='r', linestyle='--', label='Valor Varianza Esperado') 
plt.title("Número de Tiradas sobre Valor Varianza acumulada en una corrida")
plt.xlabel("Número de tiradas")
plt.ylabel("Valor Varianza")
plt.legend()
plt.show()



# --------- Graficos de comparación del NUMERO ELEGIDO por tirada de 1 corrida ---------
# Grafico 1
# Dibuja el gráfico de frecuencia relativa para el NUMERO ELEGIDO a lo largo de las tiradas de una corrida
plt.plot(range(1, tiradas+1), fr_a[0][numero_elegido], label=f'Frecuencia Relativa del número {numero_elegido}')
plt.axhline(y=fr_e, color='r', linestyle='--', label='Frecuencia Relativa Esperada')
plt.title(f"Número de Tiradas sobre Frecuencia Relativa acumulada del {numero_elegido}  para una corrida")
plt.xlabel("Número de tiradas") 
plt.ylabel("Frecuencia Relativa")
plt.legend()
plt.show()



# --------- Graficos de comparación por corrida ---------
# estos son para ver que los valores de cada corrida efectivamente son cercanos a los valores esperados

def graficar_regla_empirica(datos):
    mean = np.mean(datos)
    std = np.std(datos)
    plt.axhline(y=mean + std, color='g', linestyle=':', alpha=0.7, label=r'$\mu \pm 1\sigma$ (68%)')
    plt.axhline(y=mean - std, color='g', linestyle=':', alpha=0.7)
    plt.axhline(y=mean + 2*std, color='orange', linestyle=':', alpha=0.7, label=r'$\mu \pm 2\sigma$ (95%)')
    plt.axhline(y=mean - 2*std, color='orange', linestyle=':', alpha=0.7)
    plt.axhline(y=mean + 3*std, color='purple', linestyle=':', alpha=0.7, label=r'$\mu \pm 3\sigma$ (99.7%)')
    plt.axhline(y=mean - 3*std, color='purple', linestyle=':', alpha=0.7)

# Grafico 1: Gráfico de bastones - Frecuencia Absoluta
conteos_totales = np.sum(fa, axis=0) # Sumar la frecuencia absoluta de todos los números en todas las corridas
plt.stem(range(cant_numeros_ruleta), conteos_totales)
plt.title("Gráfico de Bastones - Frecuencia Absoluta de cada número en todas las corridas")
plt.xlabel("Valores de la Ruleta")
plt.ylabel("Cantidad de veces que salió")
plt.show()

# Grafico 2: Grafico Scatter (Dispersión) - Frecuencia relativa del numero elegido por corrida
x_corridas = range(1, corridas + 1) # Eje x con el número de corridas (1, 2, ..., corridas)
fr_corridas = [corrida[numero_elegido][-1] for corrida in fr_a]
plt.scatter(x_corridas, fr_corridas, alpha=0.5, s=10, label=f'Frecuencia Relativa del número {numero_elegido}')
plt.axhline(y=fr_e, color='r', linestyle='--', linewidth=2, label='Frecuencia Relativa Esperada')
graficar_regla_empirica(fr_corridas)
plt.title("Gráfico de Dispersión - Número de Corridas sobre Frecuencia Relativa")
plt.xlabel("Número de corridas")
plt.ylabel("Frecuencia Relativa")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Grafico 3: Grafico Scatter (Dispersión) - Promedio por corrida
vp_corridas = [corrida[-1] for corrida in vp_a]
plt.scatter(x_corridas, vp_corridas, alpha=0.5, s=10, label='Valor Promedio')
plt.axhline(y=vp_e, color='r', linestyle='--', linewidth=2, label='Valor Promedio Esperado')
graficar_regla_empirica(vp_corridas)
plt.title("Gráfico de Dispersión - Número de Corridas sobre Valor Promedio")
plt.xlabel("Número de corridas")
plt.ylabel("Valor Promedio")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Grafico 4: Grafico Scatter (Dispersión) - Desvio estandar por corrida
vd_corridas = [corrida[-1] for corrida in vd_a]
plt.scatter(x_corridas, vd_corridas, alpha=0.5, s=10, label='Valor Desvio')
plt.axhline(y=desv_e, color='r', linestyle='--', linewidth=2, label='Valor Desvio Esperado')
graficar_regla_empirica(vd_corridas)
plt.title("Gráfico de Dispersión - Número de Corridas sobre Valor Desvio")
plt.xlabel("Número de corridas")
plt.ylabel("Valor Desvio")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

# Grafico 5: Grafico Scatter (Dispersión) - Varianza por corrida
vv_corridas = [corrida[-1] for corrida in vv_a]
plt.scatter(x_corridas, vv_corridas, alpha=0.5, s=10, label='Valor Varianza')
plt.axhline(y=vari_e, color='r', linestyle='--', linewidth=2, label='Valor Varianza Esperado')
graficar_regla_empirica(vv_corridas)
plt.title("Gráfico de Dispersión - Número de Corridas sobre Valor Varianza")
plt.xlabel("Número de corridas")
plt.ylabel("Valor Varianza")
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()





















#-------------------------------------------------------------
#---------------- GRAFICOS MAS DE UNA CORRIDA ----------------

# ---------- Graficos de tendencia de la distribución de los valores (TCL) a lo largo de las corridas ----------
# Grafico 1
# Dibuja el histograma de los promedios finales de cada corrida

#calculo promedio de los promedios finales de cada corrida
promedios_ultima_tirada = [promedios_corrida[-1] for promedios_corrida in vp_a]
promedio_ultima_tirada = float(np.mean(promedios_ultima_tirada))
print(f"Promedio de los promedios finales de cada corrida: {promedio_ultima_tirada}")

#calculo desvio de los promedios finales de cada corrida
desvio_ultima_tirada = float(np.std(promedios_ultima_tirada))
print(f"Desvio de los promedios finales de cada corrida: {desvio_ultima_tirada}")

plt.hist(promedios_ultima_tirada, bins='auto', color='skyblue', edgecolor='black', alpha=0.7)
plt.axvline(promedio_ultima_tirada, color='red', linestyle='dashed', linewidth=2, label=f'Media: {promedio_ultima_tirada:.2f}')
plt.axvline(vp_e, color='blue', linestyle='dotted', linewidth=2, label=f'Esperada: {vp_e:.4f}')


# Formateo del gráfico
plt.title(f'Distribución de {corridas} promedios (n={tiradas} tiradas/corrida)')
plt.xlabel('Valor del promedio')
plt.ylabel('Frecuencia (cantidad de corridas)')
plt.legend()
plt.grid(axis='y', alpha=0.3)

plt.show()

#Grafico 2
# TCL para la frecuencia relativa del numero elegido
frecuencias_finales = [fr_c[numero_elegido][-1] for fr_c in fr_a]
frecuencia_final_promedio = float(np.mean(frecuencias_finales))
print(f"Promedio de las frecuencias relativas finales del número elegido: {frecuencia_final_promedio}")
desvio_frecuencia_final = float(np.std(frecuencias_finales))
print(f"Desvio de las frecuencias relativas finales del número elegido: {desvio_frecuencia_final}")


plt.hist(frecuencias_finales, bins='auto', color='lightgreen', edgecolor='black', alpha=0.7)
plt.axvline(frecuencia_final_promedio, color='red', linestyle='dashed', linewidth=2, label=f'Media: {frecuencia_final_promedio:.4f}')
plt.axvline(fr_e, color='blue', linestyle='dotted', linewidth=2, label=f'Esperada: {fr_e:.4f}')
plt.title(f'Distribución de {corridas} frecuencias relativas (n={tiradas} tiradas/corrida)')
plt.xlabel('Valor de la frecuencia relativa')
plt.ylabel('Frecuencia (cantidad de corridas)')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.show()


print("")
varianza_obtenida = float(np.mean([corrida[-1] for corrida in vv_a]))
desvio_obtenido = float(np.mean([corrida[-1] for corrida in vd_a]))
print(f"Frecuencia relativa obtenida: {frecuencia_final_promedio:.4f}")
print(f"Promedio obtenido: {promedio_ultima_tirada:.4f}")
print(f"Varianza obtenida: {varianza_obtenida:.4f}")
print(f"Desvío estándar obtenido: {desvio_obtenido:.4f}")
