import matplotlib.pyplot as plt
import numpy as np
import random
import math

def grafico_uniforme_rechazo(a=0, b=10, candidatos_totales=500):
    # Listas separadas para guardar las coordenadas de los buenos y los malos
    aceptados_x = []
    aceptados_y = []
    
    rechazados_x = []
    rechazados_y = []

    for _ in range(candidatos_totales):
        r1 = random.random()  # Eje X (0 a 1)
        
        r2 = random.random() 
        
        # Transformamos r1 al rango [a, b]
        x_candidato = a + (b - a) * r1
        
        # El techo de la uniforme escalada es constante en 1.0
        techo = 1.0
        
        # Filtro de Aceptación/Rechazo
        if r2 <= techo:
            aceptados_x.append(x_candidato)
            aceptados_y.append(r2)
        else:
            rechazados_x.append(x_candidato)
            rechazados_y.append(r2)

    print(f"De {candidatos_totales} intentos, se aceptaron {len(aceptados_x)} números uniformes. Porcentaje de aceptación: {len(aceptados_x) / candidatos_totales * 100:.2f}%")

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

    print(f"De {candidatos_totales} intentos, se aceptaron {len(aceptados_x)} números normales. Porcentaje de aceptación: {len(aceptados_x) / candidatos_totales * 100:.2f}%")

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



def poisson_inversa(lamda=3, cantidad=1000):
    dist_poisson = []
    
    for _ in range(cantidad):
        R = random.random()
        x = 0
        
        probabilidad = math.exp(-lamda)
        suma_acumulada = probabilidad
        
        while R > suma_acumulada:
            x += 1
            probabilidad = probabilidad * (lamda / x)
            suma_acumulada += probabilidad
            
        dist_poisson.append(x)
        
    datos_generados = dist_poisson
    
    valores_unicos, conteos = np.unique(datos_generados, return_counts=True)
    frecuencias = conteos / cantidad 
    
    # --- GRÁFICO ---
    plt.figure(figsize=(10, 6))
    
    plt.bar(valores_unicos, frecuencias, color='lightgreen', edgecolor='black', alpha=0.7, label='Generados (Empírica)')
    
    x_teorica = np.arange(0, max(valores_unicos) + 1)
    y_teorica = [(math.exp(-lamda) * (lamda ** k)) / math.factorial(k) for k in x_teorica]
    plt.stem(x_teorica, y_teorica, linefmt='red', markerfmt='ro', basefmt=' ', label='Fórmula Teórica')
    
    # Estética
    plt.title(f'Testeo de Generador Poisson (λ={lamda})', fontsize=14)
    plt.xlabel('Número de Ocurrencias (k)', fontsize=12)
    plt.ylabel('Probabilidad P(X=k)', fontsize=12)
    
    plt.xticks(x_teorica)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

poisson_inversa(lamda=3, cantidad=1000)


def binomial_inversa(n=10, p=0.5, cantidad=1000):
    dist_binomial = []
    
    for _ in range(cantidad):
        R = random.random()
        x = 0
        
        probabilidad = (math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x)))
        suma_acumulada = probabilidad
        
        while R > suma_acumulada:
            x += 1
            if x > n:  
                break
            probabilidad = (math.comb(n, x) * (p ** x) * ((1 - p) ** (n - x)))
            suma_acumulada += probabilidad
            
        dist_binomial.append(x)
        
    datos_generados = dist_binomial
    
    valores_unicos, conteos = np.unique(datos_generados, return_counts=True)
    frecuencias = conteos / cantidad 
    
    # --- GRÁFICO ---
    plt.figure(figsize=(10, 6))
    
    plt.bar(valores_unicos, frecuencias, color='lightblue', edgecolor='black', alpha=0.7, label='Generados (Empírica)')
    
    x_teorica = np.arange(0, n + 1)
    y_teorica = [math.comb(n, k) * (p ** k) * ((1 - p) ** (n - k)) for k in x_teorica]
    plt.stem(x_teorica, y_teorica, linefmt='red', markerfmt='ro', basefmt=' ', label='Fórmula Teórica')
    
    plt.title(f'Testeo de Generador Binomial (n={n}, p={p})', fontsize=14)
    plt.xlabel('Número de Éxitos (k)', fontsize=12)
    plt.ylabel('Probabilidad P(X=k)', fontsize=12)
    
    plt.xticks(x_teorica) 
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

binomial_inversa(n=10, p=0.5, cantidad=1000)


def empirica_discreta_inversa(valores, probabilidades, cantidad=1000):
    if not math.isclose(sum(probabilidades), 1.0):
        print("Error: Las probabilidades no suman 1. Revisá tu lista.")
        return

    dist_empirica = []
    
    for _ in range(cantidad):
        R = random.random()
        suma_acumulada = 0.0
        
        for i in range(len(valores)):
            suma_acumulada += probabilidades[i]
            
            if R <= suma_acumulada:
                dist_empirica.append(valores[i])
                break 
                
    # --- TESTEO VISUAL ---
    valores_unicos, conteos = np.unique(dist_empirica, return_counts=True)
    frecuencias = conteos / cantidad 
    
    plt.figure(figsize=(10, 6))
    
    plt.bar(valores_unicos, frecuencias, color='lightgreen', edgecolor='black', alpha=0.7, label='Generados (Empírica)')
    
    plt.stem(valores, probabilidades, linefmt='red', markerfmt='ro', basefmt=' ', label='Probabilidades Teóricas')
    
    plt.title('Testeo de Generador: Empírica Discreta', fontsize=14)
    plt.xlabel('Valores Posibles (X)', fontsize=12)
    plt.ylabel('Probabilidad P(X)', fontsize=12)
    plt.xticks(valores)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    plt.legend()
    plt.show()

    return dist_empirica

mis_valores = [0, 1, 2, 3] 
mis_probabilidades = [0.40, 0.35, 0.20, 0.05] 
empirica_discreta_inversa(mis_valores, mis_probabilidades, cantidad=1000)




