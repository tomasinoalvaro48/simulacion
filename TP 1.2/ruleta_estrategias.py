import numpy as np # pip install matplotlib: libreria con numpy y pyplot
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator 
import argparse

# --------------- Manejo de argumentos de linea de comandos al ejecutar el script ---------------
# python ruleta_estrategias.py -n XXX -c YYY -s -a
parser = argparse.ArgumentParser(description='Simulación de Ruleta.')
parser.add_argument('-n', '--muestras', type=int, required=True, help='Cantidad de muestras por corrida')
parser.add_argument('-c', '--corridas', type=int, required=True, help='Cantidad de corridas/simulaciones')
parser.add_argument('-s', '--estrategia', type=str, required=True, help='Estrategia a utilizar')
parser.add_argument('-a', '--tipocapital', type=str, required=True, help='Capital a utilizar: i (infinito) o f (finito)')

# ----------- Definicion de constantes y variables -----------
# Caracteristicas de la simulacion
args = parser.parse_args()
tiradas = args.muestras
corridas = args.corridas
estrategia = args.estrategia
tipo_capital = args.tipocapital
dinero_inicial = 100

# Caracteristicas de la ruleta
cant_numeros_ruleta = 37 # Números del 0 al 36
valores_ruleta = np.arange(cant_numeros_ruleta) # Array con los valores 0 a 36 de la ruleta
par = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
impar = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]

# --------- Datos Esperados ---------
fr_e = len(par)/cant_numeros_ruleta # Frecuencia absoluta esperada
vp_e = tiradas*fr_e # Valor promedio esperado



# ----------- Inicio de la simulación -----------
dinero_martingala = []
dinero_fibonacci = []
dinero_dalembert = []
dinero_paroli = []

def ensure_fibonacci(seq, index):
    while index >= len(seq):
        seq.append(seq[-1] + seq[-2])

print(f"Simulando {corridas} corridas de {tiradas} tiradas con estrategia {estrategia} y tipo de capital {tipo_capital}...")
print("")

for c in range(corridas):
    print(f"Corrida {c + 1}...")
    valores = np.random.randint(0, cant_numeros_ruleta, tiradas)

    # ------------ Estrategia Martingala ------------
    if(estrategia == 'm'):
        dinero_martingala_corrida = []
        ganancias_martingala_corrida = []
        dinero_martingala_corrida.append(dinero_inicial)
        apuesta_martingala = 1  # Apuesta inicial
        nro_tirada = 0
        bancarrota_martingala = False
        
        while nro_tirada < tiradas and not bancarrota_martingala:
            if valores[nro_tirada] in par:
                dinero_martingala_corrida.append(dinero_martingala_corrida[-1] + apuesta_martingala)  # Ganancia
                ganancias_martingala_corrida.append(apuesta_martingala)
                apuesta_martingala = 1  # Vuelve a la apuesta inicial
            else:
                dinero_martingala_corrida.append(dinero_martingala_corrida[-1] - apuesta_martingala)  # Pérdida
                ganancias_martingala_corrida.append(-apuesta_martingala)
                apuesta_martingala *= 2  # Dobla la apuesta para la próxima tirada
            nro_tirada += 1
            if (tipo_capital == 'f' and (dinero_martingala_corrida[-1] < 0 or apuesta_martingala > dinero_martingala_corrida[-1])):
                bancarrota_martingala = True

        if tipo_capital == 'i':
            dinero_martingala.append(ganancias_martingala_corrida)  # Guarda ganancia/pérdida por tirada en esta corrida
        else:
            dinero_martingala.append(dinero_martingala_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
        print(f"Dinero final MARTINGALA después de {tiradas} tiradas: {dinero_martingala_corrida}")
        if dinero_martingala_corrida[-1] > dinero_inicial:
            print("¡Ganancia!")
        elif dinero_martingala_corrida[-1] < dinero_inicial:
            print("Pérdida.")
        if bancarrota_martingala:
            print("¡Quedaste en bancarrota!")


    

    # ------------ Estrategia Fibonacci ------------
    if(estrategia == 'f'):
        dinero_fibonacci_corrida = []
        ganancias_fibonacci_corrida = []

        dinero_fibonacci_corrida.append(dinero_inicial)
        posicion_secuencia = 0
        bancarrota_fibonacci = False
        
        # Secuencia Fibonacci base; se expande dinamicamente con función ensure_fibonacci()
        s_fibonacci = [1, 1]
        
        nro_tirada = 0
        while nro_tirada < tiradas and not bancarrota_fibonacci:
            ensure_fibonacci(s_fibonacci, posicion_secuencia)
            if valores[nro_tirada] in par:
                dinero_fibonacci_corrida.append(dinero_fibonacci_corrida[-1] + s_fibonacci[posicion_secuencia])  # Ganancia
                ganancias_fibonacci_corrida.append(s_fibonacci[posicion_secuencia])
                posicion_secuencia = max(posicion_secuencia - 2, 0)  # Retrocede dos posiciones, pero no puede ser menor a 0
            else:
                dinero_fibonacci_corrida.append(dinero_fibonacci_corrida[-1] - s_fibonacci[posicion_secuencia])  # Pérdida
                ganancias_fibonacci_corrida.append(-s_fibonacci[posicion_secuencia])
                posicion_secuencia = posicion_secuencia + 1 # Avanza un número
            nro_tirada += 1
            ensure_fibonacci(s_fibonacci, posicion_secuencia)
            if (tipo_capital == 'f' and (dinero_fibonacci_corrida[-1] < 0 or s_fibonacci[posicion_secuencia] > dinero_fibonacci_corrida[-1])):
                bancarrota_fibonacci = True

        if tipo_capital == 'i':
            dinero_fibonacci.append(ganancias_fibonacci_corrida)  # Guarda ganancia/pérdida por tirada en esta corrida
        else:
            dinero_fibonacci.append(dinero_fibonacci_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
        print(f"Dinero final FIBONACCI después de {tiradas} tiradas: {dinero_fibonacci_corrida}")  
        if dinero_fibonacci_corrida[-1] > dinero_inicial:
            print("¡Ganancia!")
        elif dinero_fibonacci_corrida[-1] < dinero_inicial:
            print("Pérdida.")
        if bancarrota_fibonacci:
            print("¡Quedaste en bancarrota!")



    # ------------ Estrategia D’Alembert ------------
    if(estrategia == 'd'):
        dinero_dalembert_corrida = []
        ganancias_dalembert_corrida = []
        dinero_dalembert_corrida.append(dinero_inicial)
        nro_tirada = 0
        apuesta = 1  # Apuesta inicial
        arr_dalembert = []
        bancarrota_dalembert = False

        while nro_tirada < tiradas and not bancarrota_dalembert:
            if(len(arr_dalembert) == 0):
                arr_dalembert = [1,1,1,1,1,1,1,1,1,1]  # Apuesta inicial

            apuesta = arr_dalembert[0] + arr_dalembert[-1]  # Apuesta actual es la suma del primer y último número de la secuencia
            if valores[nro_tirada] in par:
                dinero_dalembert_corrida.append(dinero_dalembert_corrida[-1] + apuesta)  # Ganancia
                ganancias_dalembert_corrida.append(apuesta)
                arr_dalembert.pop(0)  # Elimina el primer número de la fila
                if len(arr_dalembert) > 0:
                    arr_dalembert.pop(-1)  # Elimina el último número de la fila
            else:
                dinero_dalembert_corrida.append(dinero_dalembert_corrida[-1] - apuesta)  # Pérdida
                ganancias_dalembert_corrida.append(-apuesta)
                arr_dalembert.append(apuesta)
            nro_tirada += 1
            if (tipo_capital == 'f' and (dinero_dalembert_corrida[-1] < 0 or apuesta > dinero_dalembert_corrida[-1])):
                bancarrota_dalembert = True

        if tipo_capital == 'i':
            dinero_dalembert.append(ganancias_dalembert_corrida)  # Guarda ganancia/pérdida por tirada en esta corrida
        else:
            dinero_dalembert.append(dinero_dalembert_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
        print(f"Dinero final después de {tiradas} tiradas: {dinero_dalembert_corrida}")
        if dinero_dalembert_corrida[-1] > dinero_inicial:
            print("¡Ganancia!")
        elif dinero_dalembert_corrida[-1] < dinero_inicial:
            print("Pérdida.")
        if bancarrota_dalembert:
            print("¡Quedaste en bancarrota!")


    # --------------- Estrategia Paroli - Elegida por el Grupo --------------- 
    if (estrategia == 'o'):
        apuesta_paroli = 1
        dinero_paroli_corrida = []
        ganancias_paroli_corrida = []
        dinero_paroli_corrida.append(dinero_inicial)
        bancarrota_paroli = False
        
        acumulador_ganancias_seguidas = 0
        nro_tirada = 0

        while nro_tirada < tiradas and not bancarrota_paroli:
            if valores[nro_tirada] in par:
                dinero_paroli_corrida.append(dinero_paroli_corrida[-1] + apuesta_paroli)
                ganancias_paroli_corrida.append(apuesta_paroli)
                acumulador_ganancias_seguidas += 1
                apuesta_paroli *= 2
            else:
                dinero_paroli_corrida.append(dinero_paroli_corrida[-1] - apuesta_paroli)
                ganancias_paroli_corrida.append(-apuesta_paroli)
                apuesta_paroli = 1
                acumulador_ganancias_seguidas = 0
            nro_tirada += 1
            # Reiniciar apuesta cuando se alcanzan 3 ganancias seguidas antes de chequear bancarrota
            if acumulador_ganancias_seguidas == 3:  # Si se alcanzan 3 ganancias seguidas, se reinicia la apuesta
                apuesta_paroli = 1
                acumulador_ganancias_seguidas = 0

            # Comprobación de bancarrota con la apuesta que realmente se usará la próxima ronda
            if (tipo_capital == 'f' and (dinero_paroli_corrida[-1] < 0 or apuesta_paroli > dinero_paroli_corrida[-1])):
                bancarrota_paroli = True

        if tipo_capital == 'i':
            dinero_paroli.append(ganancias_paroli_corrida)  # Guarda ganancia/pérdida por tirada en esta corrida
        else:
            dinero_paroli.append(dinero_paroli_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
        print(f"Dinero final después de {tiradas} tiradas: {dinero_paroli_corrida}")
        if dinero_paroli_corrida[-1] > dinero_inicial:
            print("¡Ganancia!")
        elif dinero_paroli_corrida[-1] < dinero_inicial:
            print("Pérdida.")
        if bancarrota_paroli:
            print("¡Quedaste en bancarrota!")



'''
    # ------------ Estrategia Elegida por el grupo: HOLLANDISH ------------
    apuesta_inicial_hollandish = 1
    dinero_hollandish_corrida = []
    dinero_hollandish_corrida.append(dinero_inicial)
    bancarrota_hollandish = False
    while nro_tirada < tiradas and not bancarrota_hollandish:
        if valores[nro_tirada] in par:
            dinero_hollandish_corrida.append(dinero_hollandish_corrida[-1] + apuesta_inicial_hollandish)
            if apuesta_inicial_hollandish > 1:
                apuesta_inicial_hollandish -= 1
        else:
           dinero_hollandish_corrida.append(dinero_hollandish_corrida[-1] - apuesta_inicial_hollandish)
           apuesta_inicial_hollandish += 1
        nro_tirada +=1
'''

# ----------- Graficos de Resultados -----------
# Convergencia del porcentaje de victorias al 48,6%
victorias_acum = np.cumsum(np.isin(valores, par))
n_tiradas = np.arange(1, len(valores) + 1)
porcentaje_victorias = victorias_acum / n_tiradas

plt.plot(n_tiradas, porcentaje_victorias, color="teal", label="Porcentaje observado")
plt.axhline(y=len(par) / cant_numeros_ruleta, color="gray", linestyle="--", label="48.6% teorico")
plt.title("Convergencia del porcentaje de victorias")
plt.xlabel("Numero de tiradas")
plt.ylabel("Porcentaje de victorias")
plt.gca().yaxis.set_major_locator(MaxNLocator(integer=False))
plt.legend()
plt.tight_layout()
plt.show()

# DINERO FINITO
if tipo_capital == 'f':
    # Martingala
    if estrategia == 'm':
        # Flujo de caja 
        plt.plot(range(len(dinero_martingala_corrida)), dinero_martingala_corrida, label='fc (flujo de caja)')
        if len(dinero_martingala_corrida) <= tiradas:
            plt.scatter(len(dinero_martingala_corrida) - 1, dinero_martingala_corrida[-1], color='black', zorder=5, label='Bancarrota')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial') 
        plt.title("Flujo de caja 1ra corrida - Martingala") 
        plt.xlabel("Número de tiradas") 
        plt.ylabel("cc (Cantidad de capital)") 
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend() 
        plt.show()

        # Dispercion de Dinero Final por Corrida
        plt.scatter(range(1, len(dinero_martingala) + 1), dinero_martingala, color='blue', alpha=0.7, s=20, label='Martingala')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
        plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (Martingala)")
        plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
        plt.ylabel("Dinero Final al terminar las tiradas")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

        #Promedio de Ganancia/Pérdida 
        promedio_final_martingala = np.mean(dinero_martingala)
        ganancia_promedio = promedio_final_martingala - dinero_inicial

        print(f"La ganancia/pérdida promedio de la Martingala es: {ganancia_promedio}")
        etiquetas = ['Capital Inicial', 'Promedio Final']
        valores = [dinero_inicial, promedio_final_martingala]
        color_final = 'green' if ganancia_promedio > 0 else 'red'
        colores = ['blue', color_final]
        plt.bar(etiquetas, valores, color=colores, width=0.5)
        plt.axhline(y=dinero_inicial, color='gray', linestyle='--', label='Punto de equilibrio')
        for i, valor in enumerate(valores):
            plt.text(i, valor + 2, f"${valor:.2f}", ha='center', fontweight='bold')
        plt.title("Rendimiento Promedio de la Estrategia Martingala")
        plt.ylabel("Capital (cc)")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend()
        plt.show()

    # Fibonacci
    if estrategia == 'f':
        # Flujo de caja
        plt.plot(range(len(dinero_fibonacci_corrida)), dinero_fibonacci_corrida, label='fc (flujo de caja)')
        if len(dinero_fibonacci_corrida) <= tiradas:
            plt.scatter(len(dinero_fibonacci_corrida) - 1, dinero_fibonacci_corrida[-1], color='black', zorder=5, label='Bancarrota')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial') 
        plt.title("Flujo de caja 1ra corrida - Fibonacci") 
        plt.xlabel("Número de tiradas") 
        plt.ylabel("cc (Cantidad de capital)") 
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend() 
        plt.show()

        # Dispercion de Dinero Final por Corrida
        plt.scatter(range(1, len(dinero_fibonacci) + 1), dinero_fibonacci, color='green', alpha=0.7, s=20, label='Fibonacci', marker='^')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
        plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (Fibonacci)")
        plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
        plt.ylabel("Dinero Final al terminar las tiradas")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

        #Promedio de Ganancia/Pérdida
        promedio_final_fibonacci = np.mean(dinero_fibonacci)
        ganancia_promedio = promedio_final_fibonacci - dinero_inicial

        print(f"La ganancia/pérdida promedio de la Fibonacci es: {ganancia_promedio}")
        etiquetas = ['Capital Inicial', 'Promedio Final']
        valores = [dinero_inicial, promedio_final_fibonacci]
        color_final = 'green' if ganancia_promedio > 0 else 'red'
        colores = ['blue', color_final]
        plt.bar(etiquetas, valores, color=colores, width=0.5)
        plt.axhline(y=dinero_inicial, color='gray', linestyle='--', label='Punto de equilibrio')
        for i, valor in enumerate(valores):
            plt.text(i, valor + 2, f"${valor:.2f}", ha='center', fontweight='bold')
        plt.title("Rendimiento Promedio de la Estrategia Fibonacci")
        plt.ylabel("Capital (cc)")
        plt.legend()
        plt.show()

    # D'Alembert
    if estrategia == 'd':
        # Flujo de caja
        plt.plot(range(len(dinero_dalembert_corrida)), dinero_dalembert_corrida, label='fc (flujo de caja)')
        if len(dinero_dalembert_corrida) <= tiradas:
            plt.scatter(len(dinero_dalembert_corrida) - 1, dinero_dalembert_corrida[-1], color='black', zorder=5, label='Bancarrota')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial') 
        plt.title("Flujo de caja 1ra corrida - D'Alembert") 
        plt.xlabel("Número de tiradas") 
        plt.ylabel("cc (Cantidad de capital)") 
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend() 
        plt.show()

        # Dispercion de Dinero Final por Corrida
        plt.scatter(range(1, len(dinero_dalembert) + 1), dinero_dalembert, color='orange', alpha=0.7, s=20, label='D\'Alembert', marker='s')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
        plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (D'Alembert)")
        plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
        plt.ylabel("Dinero Final al terminar las tiradas")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

        #Promedio de Ganancia/Pérdida
        promedio_final_dalembert = np.mean(dinero_dalembert)
        ganancia_promedio = promedio_final_dalembert - dinero_inicial

        print(f"La ganancia/pérdida promedio de la D'Alembert es: {ganancia_promedio}")
        etiquetas = ['Capital Inicial', 'Promedio Final']
        valores = [dinero_inicial, promedio_final_dalembert]
        color_final = 'green' if ganancia_promedio > 0 else 'red'
        colores = ['blue', color_final]
        plt.bar(etiquetas, valores, color=colores, width=0.5)
        plt.axhline(y=dinero_inicial, color='gray', linestyle='--', label='Punto de equilibrio')
        for i, valor in enumerate(valores):
            plt.text(i, valor + 2, f"${valor:.2f}", ha='center', fontweight='bold')
        plt.title("Rendimiento Promedio de la Estrategia D'Alembert")
        plt.ylabel("Capital (cc)")
        plt.legend()
        plt.show()
    
    # Paroli
    if estrategia == 'o':
        # Flujo de caja
        plt.plot(range(len(dinero_paroli_corrida)), dinero_paroli_corrida, label='fc (flujo de caja)')
        if len(dinero_paroli_corrida) <= tiradas:
            plt.scatter(len(dinero_paroli_corrida) - 1, dinero_paroli_corrida[-1], color='black', zorder=5, label='Bancarrota') 
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial')
        plt.title("Flujo de caja 1ra corrida - Paroli")
        plt.xlabel("Número de tiradas")
        plt.ylabel("cc (Cantidad de capital)")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend()
        plt.show()

        # Dispercion de Dinero Final por Corrida
        plt.scatter(range(1, len(dinero_paroli) + 1), dinero_paroli, color='purple', alpha=0.7, s=20, label='Paroli', marker='D')
        plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
        plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (Paroli)")
        plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
        plt.ylabel("Dinero Final al terminar las tiradas")
        plt.gca().xaxis.set_major_locator(MaxNLocator(integer=True))
        plt.legend(loc='best')
        plt.tight_layout()
        plt.show()

        #Promedio de Ganancia/Pérdida 
        promedio_final_paroli = np.mean(dinero_paroli)
        ganancia_promedio = promedio_final_paroli - dinero_inicial

        print(f"La ganancia/pérdida promedio de la Paroli es: {ganancia_promedio}")
        etiquetas = ['Capital Inicial', 'Promedio Final']
        valores = [dinero_inicial, promedio_final_paroli]
        color_final = 'green' if ganancia_promedio > 0 else 'red'
        colores = ['blue', color_final]
        plt.bar(etiquetas, valores, color=colores, width=0.5)
        plt.axhline(y=dinero_inicial, color='gray', linestyle='--', label='Punto de equilibrio')
        for i, valor in enumerate(valores):
            plt.text(i, valor + 2, f"${valor:.2f}", ha='center', fontweight='bold')
        plt.title("Rendimiento Promedio de la Estrategia Paroli ")
        plt.ylabel("Capital (cc)")
        plt.legend()
        plt.show()


# DINERO INFINITO
else:
    if estrategia == 'f':
        # Sumatoria de ganancia vs perdida (sin capital inicial) - Fibonacci
        resultados_corrida = dinero_fibonacci[0] if len(dinero_fibonacci) > 0 else []
        n_tiradas = np.arange(1, len(resultados_corrida) + 1)
        ganancia_acum = np.cumsum(np.where(np.array(resultados_corrida) > 0, resultados_corrida, 0))
        perdida_acum = np.cumsum(np.where(np.array(resultados_corrida) < 0, -np.array(resultados_corrida), 0))

        plt.plot(n_tiradas, ganancia_acum, color="seagreen", label="Ganancia acumulada")
        plt.plot(n_tiradas, perdida_acum, color="firebrick", label="Perdida acumulada")
        plt.title("Sumatoria de ganancia vs perdida (Fibonacci, 1 corrida)")
        plt.xlabel("Numero de tiradas")
        plt.ylabel("Unidades acumuladas")
        plt.legend()
        plt.tight_layout()
        plt.show()

    if estrategia == 'm':
        # Sumatoria de ganancia vs perdida (sin capital inicial) - Martingala
        resultados_corrida = dinero_martingala[0] if len(dinero_martingala) > 0 else []
        n_tiradas = np.arange(1, len(resultados_corrida) + 1)
        ganancia_acum = np.cumsum(np.where(np.array(resultados_corrida) > 0, resultados_corrida, 0))
        perdida_acum = np.cumsum(np.where(np.array(resultados_corrida) < 0, -np.array(resultados_corrida), 0))

        plt.plot(n_tiradas, ganancia_acum, color="seagreen", label="Ganancia acumulada")
        plt.plot(n_tiradas, perdida_acum, color="firebrick", label="Perdida acumulada")
        plt.title("Sumatoria de ganancia vs perdida (Martingala, 1 corrida)")
        plt.xlabel("Numero de tiradas")
        plt.ylabel("Unidades acumuladas")
        plt.legend()
        plt.tight_layout()
        plt.show()

    if estrategia == 'd':
        # Sumatoria de ganancia vs perdida (sin capital inicial) - D'Alembert
        resultados_corrida = dinero_dalembert[0] if len(dinero_dalembert) > 0 else []
        n_tiradas = np.arange(1, len(resultados_corrida) + 1)
        ganancia_acum = np.cumsum(np.where(np.array(resultados_corrida) > 0, resultados_corrida, 0))
        perdida_acum = np.cumsum(np.where(np.array(resultados_corrida) < 0, -np.array(resultados_corrida), 0))

        plt.plot(n_tiradas, ganancia_acum, color="seagreen", label="Ganancia acumulada")
        plt.plot(n_tiradas, perdida_acum, color="firebrick", label="Perdida acumulada")
        plt.title("Sumatoria de ganancia vs perdida (D'Alembert, 1 corrida)")
        plt.xlabel("Numero de tiradas")
        plt.ylabel("Unidades acumuladas")
        plt.legend()
        plt.tight_layout()
        plt.show()

    if estrategia == 'o':
        # Sumatoria de ganancia vs perdida (sin capital inicial) - Paroli
        resultados_corrida = dinero_paroli[0] if len(dinero_paroli) > 0 else []
        n_tiradas = np.arange(1, len(resultados_corrida) + 1)
        ganancia_acum = np.cumsum(np.where(np.array(resultados_corrida) > 0, resultados_corrida, 0))
        perdida_acum = np.cumsum(np.where(np.array(resultados_corrida) < 0, -np.array(resultados_corrida), 0))

        plt.plot(n_tiradas, ganancia_acum, color="seagreen", label="Ganancia acumulada")
        plt.plot(n_tiradas, perdida_acum, color="firebrick", label="Perdida acumulada")
        plt.title("Sumatoria de ganancia vs perdida (Paroli, 1 corrida)")
        plt.xlabel("Numero de tiradas")
        plt.ylabel("Unidades acumuladas")
        plt.legend()
        plt.tight_layout()
        plt.show()