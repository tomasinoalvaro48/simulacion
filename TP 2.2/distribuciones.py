import matplotlib.pyplot as plt
import numpy as np
import random
import math



# Distribucion uniforme
# f(x) =1/b-a para a <= x <= b
'''
def uniforme(a=0, b=1, candidatos_totales=500):


    # Definimos los límites (rango finito a <= x <= b)
    

    # Aquí vamos a ir guardando los números que pasen la prueba
    dist_uniforme_rechazo = []

    for _ in range(candidatos_totales):
        
        # 1. Generamos la coordenada paso a paso
        r1 = random.random()  
        r2 = random.random()  
        
        # 2. Transformamos r1 para que caiga en nuestro rango de 0 a 1
        x_candidato = a + (b - a) * r1
        
        # 3. Definimos la altura del techo de la curva
        techo = 1.0
        
        # 4. El Filtro (Criterio de Aceptación/Rechazo)
        if r2 <= techo:
            dist_uniforme_rechazo.append((x_candidato, r1))
        else:
            pass

  


def distribucion_normal(a = -5, b = 5, candidatos_totales=500):
    dist_normal_rechazo = []

    for _ in range(candidatos_totales):
        # Generamos un número aleatorio de la distribución normal
        r_1 = random.random()  # Candidato (eje X)
        r_2 = random.random()  # Juez (eje Y)

        x_candidato = a + (b - a) * r_1

        techo_en_x = math.exp(-0.5 * (x_candidato ** 2))
            
        # 5. El Filtro (Criterio de Aceptación/Rechazo)
        if r_2 <= techo_en_x:
            dist_normal_rechazo.append(x_candidato)
        else:
            pass
        
    print(f"De {candidatos_totales} intentos, se aceptaron {len(dist_normal_rechazo)} números normales. Porcentaje de aceptación: {len(dist_normal_rechazo) / candidatos_totales * 100:.2f}%")

 ''' 
def distribucion_exponencial(lambd, candidatos_totales=500):
    a=0
    b=10
    dist_exponencial_rechazo = []

    for _ in range(candidatos_totales):

        r_1 = random.random()
        r_2 = random.random()

        x_candidato = a + (b - a) * r_1

        techo_en_x = (1/lambd)* lambd * math.exp(-lambd * x_candidato)

        if r_2 <= techo_en_x:
            dist_exponencial_rechazo.append(x_candidato)
        else:
            pass

    print(f"De {candidatos_totales} intentos, se aceptaron {len(dist_exponencial_rechazo)} números exponenciales. Porcentaje de aceptación: {len(dist_exponencial_rechazo) / candidatos_totales * 100:.2f}%")










    




def grafico_uniforme_rechazo(a=0, b=10, candidatos_totales=500):
    # Listas separadas para guardar las coordenadas de los buenos y los malos
    aceptados_x = []
    aceptados_y = []
    
    rechazados_x = []
    rechazados_y = []

    for _ in range(candidatos_totales):
        r1 = random.random()  # Eje X (0 a 1)
        
        dardo_y = random.random() 
        
        # Transformamos r1 al rango [a, b]
        x_candidato = a + (b - a) * r1
        
        # El techo de la uniforme escalada es constante en 1.0
        techo = 1.0
        
        # Filtro de Aceptación/Rechazo
        if dardo_y <= techo:
            aceptados_x.append(x_candidato)
            aceptados_y.append(dardo_y)
        else:
            rechazados_x.append(x_candidato)
            rechazados_y.append(dardo_y)

    # --- GRÁFICO ---
    plt.figure(figsize=(10, 6))

    plt.plot([a, b], [techo, techo], color='blue', linewidth=2, label='Techo f(x) = 1.0')

    plt.scatter(aceptados_x, aceptados_y, color='green', alpha=0.6, edgecolors='black', label='OK (Aceptados)')

    plt.scatter(rechazados_x, rechazados_y, color='red', alpha=0.6, edgecolors='black', label='Malos (Rechazados)')

    plt.title('Método de Rechazo: Posición real de los dardos (Uniforme)', fontsize=14)
    plt.xlabel(f'Valor Generado en X (Rango {a} a {b})', fontsize=12)
    plt.ylabel('Altura del Dardo en Y', fontsize=12)
    

    plt.xlim(a - 1, b + 1)
    plt.ylim(0, 1.05)
    
    plt.axhline(0, color='black', linewidth=0.5, linestyle='-') # Dibuja el Eje X
    plt.axvline(0, color='black', linewidth=0.5, linestyle='-') # Dibuja el Eje Y
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    plt.show()

grafico_uniforme_rechazo(0, 10, 500)


def grafico_normal_rechazo(a=-5, b=5, candidatos_totales=500):
    aceptados_x = []
    aceptados_y = []
    
    rechazados_x = []
    rechazados_y = []

    for _ in range(candidatos_totales):
        r1 = random.random()
        r2 = random.random()

        x_candidato = a + (b - a) * r1

        techo = math.exp(-0.5 * (x_candidato ** 2))

        if r2 <= techo:
            aceptados_x.append(x_candidato)
            aceptados_y.append(r2)
        else:
            rechazados_x.append(x_candidato)
            rechazados_y.append(r2) 



    # --- GRÁFICO ---
    plt.figure(figsize=(10, 6))

    x_campana = np.linspace(a, b, 200)
    y_campana = np.exp(-0.5 * (x_campana ** 2))
    plt.plot(x_campana, y_campana, color='blue', linewidth=2, label='Techo f(x) = exp(-x²/2)')

    plt.scatter(aceptados_x, aceptados_y, color='green', alpha=0.6, edgecolors='black', label='OK (Aceptados)')

    plt.scatter(rechazados_x, rechazados_y, color='red', alpha=0.6, edgecolors='black', label='Malos (Rechazados)')

    plt.title('Método de Rechazo: Posición real de los dardos (Normal)', fontsize=14)
    plt.xlabel(f'Valor Generado en X (Rango {a} a {b})', fontsize=12)
    plt.ylabel('Altura del Dardo en Y', fontsize=12)
    
    plt.xlim(a - 1, b + 1)
    plt.ylim(0, 1.05)
    
    plt.axhline(0, color='black', linewidth=0.5, linestyle='-') # Dibuja el Eje X
    plt.axvline(0, color='black', linewidth=0.5, linestyle='-') # Dibuja el Eje Y
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    plt.show()

grafico_normal_rechazo()



def grafico_exponencial_rechazo(lambd=1, a=0, b=10, candidatos_totales=500):
   
    aceptados_x = []
    aceptados_y = []
    
    rechazados_x = []
    rechazados_y = []

    for _ in range(candidatos_totales):

        r_1 = random.random()
        r_2 = random.random()

        x_candidato = a + (b - a) * r_1

        techo_en_x = (1/lambd)* lambd * math.exp(-lambd * x_candidato)

        if r_2 <= techo_en_x:
            aceptados_x.append(x_candidato)
            aceptados_y.append(r_2)
        else:
            rechazados_x.append(x_candidato)
            rechazados_y.append(r_2)

    print(f"De {candidatos_totales} intentos, se aceptaron {len(aceptados_x)} números exponenciales. Porcentaje de aceptación: {len(aceptados_x) / candidatos_totales * 100:.2f}%")

     # --- GRÁFICO ---
    plt.figure(figsize=(10, 6))

    x_campana = np.linspace(a, b, 200)
    y_campana = np.exp(-lambd * x_campana)
    plt.plot(x_campana, y_campana, color='blue', linewidth=2, label='Techo f(x) = exp(-λx)')

    plt.scatter(aceptados_x, aceptados_y, color='green', alpha=0.6, edgecolors='black', label='OK (Aceptados)')

    plt.scatter(rechazados_x, rechazados_y, color='red', alpha=0.6, edgecolors='black', label='Malos (Rechazados)')

    plt.title('Método de Rechazo: Posición real de los dardos (Exponencial)', fontsize=14)
    plt.xlabel(f'Valor Generado en X (Rango {a} a {b})', fontsize=12)
    plt.ylabel('Altura del Dardo en Y', fontsize=12)
    
    plt.xlim(a - 1, b + 1)
    plt.ylim(0, 1.05)
    
    plt.axhline(0, color='black', linewidth=0.5, linestyle='-') # Dibuja el Eje X
    plt.axvline(0, color='black', linewidth=0.5, linestyle='-') # Dibuja el Eje Y
    
    plt.grid(True, linestyle='--', alpha=0.5)
    plt.legend(loc='upper right')
    plt.show()

grafico_exponencial_rechazo()























