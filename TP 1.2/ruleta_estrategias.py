import numpy as np # pip install matplotlib: libreria con numpy y pyplot
import matplotlib.pyplot as plt
import argparse
'''
# --------------- Manejo de argumentos de linea de comandos al ejecutar el script ---------------
# python ruleta_estrategias.py -n XXX -c YYY -e ZZ -s -a
parser = argparse.ArgumentParser(description='Simulación de Ruleta.')
parser.add_argument('-n', '--muestras', type=int, required=True, help='Cantidad de muestras por corrida')
parser.add_argument('-c', '--corridas', type=int, required=True, help='Cantidad de corridas/simulaciones')
parser.add_argument('-e', '--elegido', type=int, required=True, help='Número apostado/elegido')
parser.add_argument('-s', '--estrategia', type=string, required=True, help='Estrategia a utilizar')
parser.add_argument('-a', '--tipocapital', type=string, required=True, help='Capital a utilizar: i (infinito) o f (finito)')

# ----------- Definicion de constantes y variables -----------
# Caracteristicas de la simulacion
args = parser.parse_args()
tiradas = args.muestras
corridas = args.corridas
numero_elegido = args.elegido
estrategia = args.estrategia
tipo_capital = args.tipocapital
dinero_inicial = 100
'''

tiradas = 100
corridas = 100
numero_elegido = 0
estrategia = 'f' # Estrategia a utilizar: f (fibonacci), m (martingala), d (D’Alembert), o (elegida por el grupo)
tipo_capital = 'f' # Tipo de capital a utilizar: i (infinito) o f (finito)
dinero_inicial = 100

# Caracteristicas de la ruleta
cant_numeros_ruleta = 37 # Números del 0 al 36
valores_ruleta = np.arange(cant_numeros_ruleta) # Array con los valores 0 a 36 de la ruleta
par = [2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36]
impar = [1,3,5,7,9,11,13,15,17,19,21,23,25,27,29,31,33,35]

# --------- Datos Esperados ---------
# Distribucion Binomial con n = tiradas y p = 18/37 (probabilidad de ganar apostando a par o impar)
# X~Bi(n, p)
# A: el número elegido es par
# !A: el número elegido es impar
# n ensayos de Bernoulli (éxito o fracaso), prob de éxito p = 18/37 y ensayos independientes
fr_e = len(par)/cant_numeros_ruleta # Frecuencia absoluta esperada
vp_e = tiradas*fr_e # Valor promedio esperado
desv_e = tiradas*fr_e*(1 - fr_e) # Desvio estandar esperado
vari_e = desv_e**2 # Varianza esperada






# ----------- Inicio de la simulación -----------
# Acumuladores para resultados de cada estrategia
dinero_martingala = []
dinero_fibonacci = []
dinero_dalembert = []

print(f"Simulando {corridas} corridas de {tiradas} tiradas con estrategia {estrategia} y tipo de capital {tipo_capital}...")
print("")

for c in range(corridas):
    print(f"Corrida {c + 1}...")
    valores = np.random.randint(0, cant_numeros_ruleta, tiradas)

    # ------------ Estrategia Martingala ------------
    #if(estrategia == 'm'):
    dinero_martingala_corrida = []
    dinero_martingala_corrida.append(dinero_inicial)
    apuesta_martingala = 1  # Apuesta inicial
    nro_tirada = 0
    bancarrota_martingala = False
    
    while nro_tirada < tiradas and not bancarrota_martingala:
        if valores[nro_tirada] in par:
            dinero_martingala_corrida.append(dinero_martingala_corrida[-1] + apuesta_martingala)  # Ganancia
            apuesta_martingala = 1  # Vuelve a la apuesta inicial
        else:
            dinero_martingala_corrida.append(dinero_martingala_corrida[-1] - apuesta_martingala)  # Pérdida
            apuesta_martingala *= 2  # Dobla la apuesta para la próxima tirada
        nro_tirada += 1
        if (tipo_capital == 'f' and (dinero_martingala_corrida[-1] < 0 or apuesta_martingala > dinero_martingala_corrida[-1])):
            bancarrota_martingala = True

    dinero_martingala.append(dinero_martingala_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
    print(f"Dinero final MARTINGALA después de {tiradas} tiradas: {dinero_martingala_corrida}")
    if dinero_martingala_corrida[-1] > dinero_inicial:
        print("¡Ganancia!")
    elif dinero_martingala_corrida[-1] < dinero_inicial:
        print("Pérdida.")
    if bancarrota_martingala:
        print("¡Quedaste en bancarrota!")


    
    






    # ------------ Estrategia Fibonacci ------------
    #if(estrategia == 'f'):
    dinero_fibonacci_corrida = []

    dinero_fibonacci_corrida.append(dinero_inicial)
    posicion_secuencia = 0
    bancarrota_fibonacci = False
    
    # Genera la secuencia de Fibonacci hasta que el número más grande sea menor que el dinero disponible
    s_fibonacci = [1, 1] 
    while max(s_fibonacci) < dinero_inicial:  
        s_fibonacci.append(s_fibonacci[-1] + s_fibonacci[-2])
    
    nro_tirada = 0
    while nro_tirada < tiradas and not bancarrota_fibonacci:
        if valores[nro_tirada] in par:
            dinero_fibonacci_corrida.append(dinero_fibonacci_corrida[-1] + s_fibonacci[posicion_secuencia])  # Ganancia
            posicion_secuencia = max(posicion_secuencia - 2, 0)  # Retrocede dos posiciones, pero no puede ser menor a 0
        else:
            dinero_fibonacci_corrida.append(dinero_fibonacci_corrida[-1] - s_fibonacci[posicion_secuencia])  # Pérdida
            posicion_secuencia = posicion_secuencia + 1 # Avanza un número
        nro_tirada += 1
        if (tipo_capital == 'f' and (dinero_fibonacci_corrida[-1] < 0 or s_fibonacci[posicion_secuencia] > dinero_fibonacci_corrida[-1])):
            bancarrota_fibonacci = True

    dinero_fibonacci.append(dinero_fibonacci_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
    print(f"Dinero final FIBONACCI después de {tiradas} tiradas: {dinero_fibonacci_corrida}")  
    if dinero_fibonacci_corrida[-1] > dinero_inicial:
        print("¡Ganancia!")
    elif dinero_fibonacci_corrida[-1] < dinero_inicial:
        print("Pérdida.")
    if bancarrota_fibonacci:
        print("¡Quedaste en bancarrota!")



    # ------------ Estrategia D’Alembert ------------
    #if(estrategia == 'd'):
    dinero_dalembert_corrida = []
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
            arr_dalembert.pop(0)  # Elimina el primer número de la fila
            if len(arr_dalembert) > 0:
                arr_dalembert.pop(-1)  # Elimina el último número de la fila
        else:
            dinero_dalembert_corrida.append(dinero_dalembert_corrida[-1] - apuesta)  # Pérdida
            arr_dalembert.append(apuesta)
        nro_tirada += 1
        if (tipo_capital == 'f' and (dinero_dalembert_corrida[-1] < 0 or apuesta > dinero_dalembert_corrida[-1])):
            bancarrota_dalembert = True

    dinero_dalembert.append(dinero_dalembert_corrida[-1])  # Guarda el resultado final de esta corrida en el acumulador general
    print(f"Dinero final después de {tiradas} tiradas: {dinero_dalembert_corrida}")
    if dinero_dalembert_corrida[-1] > dinero_inicial:
        print("¡Ganancia!")
    elif dinero_dalembert_corrida[-1] < dinero_inicial:
        print("Pérdida.")
    if bancarrota_dalembert:
        print("¡Quedaste en bancarrota!")



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


# Graficos de Resultados (sólo la primera corrida)

# Para Fibonacci y D'Alembert, la primera corrida ocupa desde el inicio hasta la cantidad de tiradas que se hicieron antes de terminar/bancarrota.
# Como en la primera corrida arrancan con el dinero_inicial, podemos tomar el historial hasta encontrar el siguiente 'dinero_inicial' o hasta el final.
# O más simple: tomamos las tiradas que correspondan a la primera ejecución. Para no alterar tanta lógica, tomamos la porción de la primera corrida,
# pero en el caso de Martingala, para tener el flujo de la primera necesitamos recuperar la variable (o si `corridas=1` es simplemente la lista que quedó).

plt.plot(range(len(dinero_martingala_corrida)), dinero_martingala_corrida, label='fc (flujo de caja)')
if len(dinero_martingala_corrida) <= tiradas:
    plt.scatter(len(dinero_martingala_corrida) - 1, dinero_martingala_corrida[-1], color='black', zorder=5, label='Bancarrota')
plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial') 
plt.title("Flujo de caja 1ra corrida - Martingala") 
plt.xlabel("Número de tiradas") 
plt.ylabel("cc (Cantidad de capital)") 
plt.legend() 
plt.show()

# Para Fibonacci, tomamos el flujo hasta tiradas+1 (o hasta donde haya llegado en la primera corrida)
plt.plot(range(len(dinero_fibonacci_corrida)), dinero_fibonacci_corrida, label='fc (flujo de caja)')
if len(dinero_fibonacci_corrida) <= tiradas:
    plt.scatter(len(dinero_fibonacci_corrida) - 1, dinero_fibonacci_corrida[-1], color='black', zorder=5, label='Bancarrota')
plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial') 
plt.title("Flujo de caja 1ra corrida - Fibonacci") 
plt.xlabel("Número de tiradas") 
plt.ylabel("cc (Cantidad de capital)") 
plt.legend() 
plt.show()

# Para D'Alembert
plt.plot(range(len(dinero_dalembert_corrida)), dinero_dalembert_corrida, label='fc (flujo de caja)')
if len(dinero_dalembert_corrida) <= tiradas:
    plt.scatter(len(dinero_dalembert_corrida) - 1, dinero_dalembert_corrida[-1], color='black', zorder=5, label='Bancarrota')
plt.axhline(y=dinero_inicial, color='r', linestyle='--', label='Capital Inicial') 
plt.title("Flujo de caja 1ra corrida - D'Alembert") 
plt.xlabel("Número de tiradas") 
plt.ylabel("cc (Cantidad de capital)") 
plt.legend() 
plt.show()



# Grafico de dispercion de Dinero Final por Corrida (para ver todas las corridas)

plt.scatter(range(1, len(dinero_martingala) + 1), dinero_martingala, color='blue', alpha=0.7, s=20, label='Martingala')
plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (Martingala)")
plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
plt.ylabel("Dinero Final al terminar las tiradas")
plt.legend(loc='best')
plt.tight_layout()
plt.show()

plt.scatter(range(1, len(dinero_fibonacci) + 1), dinero_fibonacci, color='green', alpha=0.7, s=20, label='Fibonacci', marker='^')
plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (Fibonacci)")
plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
plt.ylabel("Dinero Final al terminar las tiradas")
plt.legend(loc='best')
plt.tight_layout()
plt.show()

plt.scatter(range(1, len(dinero_dalembert) + 1), dinero_dalembert, color='orange', alpha=0.7, s=20, label='D\'Alembert', marker='s')
plt.axhline(y=dinero_inicial, color='r', linestyle='--', linewidth=2, label='Capital Inicial')
plt.title("Dispersión - Dinero Final obtenido en CADA Corrida (D'Alembert)")
plt.xlabel("N° de Corrida (de 1 a " + str(corridas) + ")")
plt.ylabel("Dinero Final al terminar las tiradas")
plt.legend(loc='best')
plt.tight_layout()
plt.show()


































'''
plt.bar(range(1, tiradas+1),frec_relativa,color = 'blue',label='frsa (Frecuencia relativa de obtener la apuesta favorable según n)')
plt.title("Frecuencia relativa de obtener la apuesta favorable segun n")
plt.xlabel("Número de tiradas")
plt.ylabel("fr (frecuencia relativa)")
plt.legend()
plt.show()
'''


'''
perdida --> Multiplica por 2 su apuesta anterior
Ganancia --> Vuelve a su apuesta inicial --> 1


Martingala
A primera vista, la Martingala tiene mucho sentido. Doblando tu apuesta (o más) después de cada pérdida, aseguras que cuando ganes recuperarás todas 
tus pérdidas más una ganancia extra igual a tu apuesta inicial. El hecho de que vuelvas a tu apuesta original cada vez que ganes también te ayuda a
 limitar tu inversión, manteniendo tus apuestas tan bajas como se pueda. Para acelerar el proceso y hacer que ganes rápidamente, 
 el jugador puede recuperar todas sus pérdidas y un poco más si decide triplicar su apuesta después de cada pérdida, en vez de doblarla. 
 La decisión de triplicar la apuesta después de cada pérdida no debe tomarse a la ligera, ya que aumenta exponencialmente el riesgo, tal como 
 ilustra la tabla mostrada a continuación.
'''



'''
Ganancia --> retrocede dos numeros en la secuencia
Perdida --> avanza un numero en la secuencia
Comienza en 1
 cada apuesta debe realizarse en una apuesta par que pague 1:1,  como rojo/negro o impar/par

Cómo funciona la estrategia de Fibonacci en la ruleta
La estrategia de ruleta Fibonacci utiliza la secuencia numérica de Fibonacci, que lleva el nombre del matemático italiano,
 para determinar la siguiente apuesta: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, etc. Siguiendo la secuencia, 
 cada apuesta es la suma de las dos anteriores. Con cada pérdida, se avanza al siguiente número de la secuencia, 
 y con cada ganancia se retrocede dos posiciones, o se vuelve al inicio si no se ha avanzado tanto. 
 Como no se puede empezar a apostar desde 0, se comienza con una proporción de 1 y se continúa desde ahí. 
 Lo único que hay que tener en cuenta es que cada apuesta debe realizarse en una apuesta par que pague 1:1, 
 como rojo/negro o impar/par. Esto garantiza una probabilidad más equitativa de ganar o perder y evita que 
 las pérdidas se acumulen demasiado rápido. Realizar apuestas internas con esta estrategia es muy arriesgado
   y el sistema no será efectivo.
El sistema de ruleta de Fibonacci en acción
El siguiente ejemplo muestra cómo se puede usar el sistema Fibonacci para aumentar las probabilidades de 
obtener grandes ganancias en comparación con las pérdidas. Claro que, al jugar a la ruleta, es imposible 
predecir el resultado de cada giro, y aún es posible perder consecutivamente.

Secuencia	Apostar	Resultado	Ganancia
1	            1	Perder	-$1
1, 2	        2	Perder	-$3
1, 2, 3	        3	Perder	-$6
1, 2, 3, 5	    5	Perder	-$11
1, 2, 3, 5, 8	8	Ganar	$5
1, 2, 3	        3	Perder	$2

'''


'''
Se inicia con una secuencia de 10 1 --> [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
apuesta --> se suma el primer y ultimo nro de la fila --> arr[0] + arr[-1] = apuesta
Perdida --> se agrega el ultimo nro de la fila --> arr.append(apuesta)
Ganancia --> se eliminan los dos primeros numeros de la fila --> arr.pop(0) and arr.pop(-1))


'''

'''
Hollandish
Estrategia de Ruleta Hollandish
1. La secuencia de apuestas
El sistema utiliza una progresión fija de números impares:

1 – 3 – 5 – 7 – 9 – 11... (cada número representa unidades o "fichas").

2. ¿Cómo funciona un bloque?
Haces una apuesta fija durante 3 tiradas seguidas utilizando el número de la secuencia que te corresponda.
 Al terminar el bloque de 3, evalúas el resultado global:

Si ganaste la mayoría (2 o 3 tiradas ganadas): El bloque fue exitoso. Reinicias la secuencia y vuelves a 
apostar 1 unidad.

Si perdiste la mayoría (2 o 3 tiradas perdidas): El bloque fue perdedor. Avanzas al siguiente nivel de 
la secuencia para el próximo bloque (por ejemplo, pasas de apostar 1 unidad a apostar 3 unidades por tirada).
'''