import matplotlib.pyplot as plt
import numpy as np
import random
import math



# Distribucion uniforme
# f(x) =1/b-a para a <= x <= b

def uniforme(a=0, b=1, candidatos_totales=500):


    # Definimos los límites (rango finito a <= x <= b)
    

    # Aquí vamos a ir guardando los números que pasen la prueba
    dist_uniforme_rechazo = []

    # Hacemos 500 intentos (lanzamos 500 dardos)
    for _ in range(candidatos_totales):
        
        # 1. Generamos la coordenada paso a paso
        r1 = random.random()  # El Candidato (eje X)
        r2 = random.random()  # El Juez (eje Y)
        
        # 2. Transformamos r1 para que caiga en nuestro rango de 0 a 1
        x_candidato = a + (b - a) * r1
        
        # 3. Definimos la altura del techo de la curva
        # Para una distribución uniforme escalada, el techo es siempre 1
        techo = 1.0
        
        # 4. El Filtro (Criterio de Aceptación/Rechazo)
        if r2 <= techo:
            # ¡Aceptado! Guardamos el valor X en nuestra lista
            dist_uniforme_rechazo.append(x_candidato)
        else:
            pass

    # Vemos cuántos sobrevivieron
    print(f"De {candidatos_totales} intentos, se aceptaron {len(dist_uniforme_rechazo)} números uniformes.")


def distribucion_normal(a, b, candidatos_totales=500):
    dist_normal_rechazo = []

    for _ in range(candidatos_totales):
        # Generamos un número aleatorio de la distribución normal
        r_1 = random.random()  # Candidato (eje X)
        r_2 = random.random()  # Juez (eje Y)

        x_candidato = a + (b - a) * r_1

        techo_en_x = math.exp(-0.5 * (x_candidato ** 2))
            
        # 5. El Filtro (Criterio de Aceptación/Rechazo)
        if r_2 <= techo_en_x:
            # ¡Aceptado! El dardo (Y) cayó por debajo de la campana
            dist_normal_rechazo.append(x_candidato)
        else:
            # ¡Rechazado! El dardo cayó en el espacio vacío por encima de la campana
            # A diferencia de la uniforme, ¡acá el código SÍ entra al else un montón de veces!
            pass
        
    print(f"De {candidatos_totales} intentos, se aceptaron {len(dist_normal_rechazo)} números normales. Porcentaje de aceptación: {len(dist_normal_rechazo) / candidatos_totales * 100:.2f}%")


uniforme(0, 1, 500)
distribucion_normal(-5, 5, 500)