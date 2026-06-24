import math
import random
import matplotlib.pyplot as plt

# Constantes de Estado del Servidor
BUSY = 1
IDLE = 0

# PARÁMETROS
# ===========
MEAN_INTERARRIVAL = 1.0 # Tiempo promedio entre arribos (minutos)
MEAN_SERVICE = 0.8 # Tiempo promedio de servicio (minutos)
NUM_DELAYS_REQUIRED = 10000 # Cantidad de clientes a procesar (que completan retraso e inician servicio)
QUEUE_LIMIT = float('inf') # Límite de la cola (cantidad de clientes que pueden estar en cola) M/M/1/K - float('inf') para M/M/1

RANDOM_SEED = 42 # Semilla de numeros aleatorios
OUTPUT_FILE = "mm1.out" # Nombre del archivo de salida para el reporte





# FUNCIONES
# ==========

# Generar variable aleatoria exponencial
def expon(mean):
    return random.expovariate(1.0 / mean)

# Inicializar variables
def initialize(mean_interarrival):
    state = {
        'sim_time': 0.0, # Reloj de simulación
        'server_status': IDLE,
        'num_in_q': 0,
        'time_arrival': [], # Lista con los tiempos de arribo de los clientes en cola
        'time_next_event': {
            # Evento 1: Arribo
            # Evento 2: Salida (finalización de servicio)
            1: expon(mean_interarrival),
            2: float('inf') # Infinito al inicio porque no hay clientes en el servidor
        },
        'time_last_event': 0.0, # Marcador de tiempo del último evento procesado (para promedios de tiempo)
        
        # Contadores estadísticos
        'num_custs_delayed': 0,
        'total_of_delays': 0.0,
        'total_time_in_system': 0.0,
        'area_num_in_q': 0.0,
        'area_server_status': 0.0,
        
        # Registro del tiempo acumulado en cada estado de tamaño de cola (para P(Nq = n))
        'time_in_q_state': {},
        
        # Estadísticas de arribos y bloqueos (para M/M/1/K)
        'num_custs_arrived': 0,
        'num_custs_blocked': 0,

        # Historial de métricas en el tiempo (para graficar evolución temporal)
        # Cada entrada: (sim_time, L, L_q, W, W_q)
        'history': []
    }
    return state



def timing(state):
    min_time = float('inf')
    next_event_type = 0
    
    for event_type, event_time in state['time_next_event'].items():
        if event_time < min_time:
            min_time = event_time
            next_event_type = event_type
            
    if next_event_type == 0:
        return None # si la lista de eventos está vacía, detener simulación
        
    state['sim_time'] = min_time
    return next_event_type



# Calcula las medidas de tiempo
def update_time_avg_stats(state):
    # Calcula el tiempo desde el último evento
    time_since_last_event = state['sim_time'] - state['time_last_event']
    state['time_last_event'] = state['sim_time']
    
    # Área bajo la curva del número de clientes en cola
    state['area_num_in_q'] += state['num_in_q'] * time_since_last_event
    
    # Área bajo la curva de utilización del servidor
    state['area_server_status'] += state['server_status'] * time_since_last_event
    
    # Tiempo acumulado en el tamaño de cola actual
    q_len = state['num_in_q']
    state['time_in_q_state'][q_len] = state['time_in_q_state'].get(q_len, 0.0) + time_since_last_event




def arrive(state, mean_interarrival, mean_service, queue_limit):
    # Programa el arribo del siguiente cliente
    state['time_next_event'][1] = state['sim_time'] + expon(mean_interarrival)
    
    # Registra un arribo
    state['num_custs_arrived'] += 1
    
    # Verifica si el servidor está ocupado
    if state['server_status'] == BUSY:
        # Servidor ocupado. Verifica si la cola superó el límite (cola finita K)
        if state['num_in_q'] >= queue_limit:
            # Cliente rechazado (denegación de servicio)
            state['num_custs_blocked'] += 1
        else:
            # Hay espacio en cola, se almacena el arribo y aumenta la cola
            state['num_in_q'] += 1
            state['time_arrival'].append(state['sim_time'])
    else:
        # Servidor inactivo, el cliente inicia servicio inmediatamente (espera = 0)
        state['num_custs_delayed'] += 1
        state['server_status'] = BUSY
        
        # Genera el tiempo de servicio y programa salida
        service_time = expon(mean_service)
        state['time_next_event'][2] = state['sim_time'] + service_time
        
        # Acumula estadísticas (demora = 0, tiempo en sistema = service_time)
        state['total_of_delays'] += 0.0
        state['total_time_in_system'] += service_time




def depart(state, mean_service):
    # Verifica si la cola está vacía
    if state['num_in_q'] == 0:
        # La cola está vacía, el servidor pasa a estar inactivo y se desprograma la salida
        state['server_status'] = IDLE
        state['time_next_event'][2] = float('inf')
    else:
        # La cola no está vacía, se saca al primer cliente
        state['num_in_q'] -= 1
        arrival_time = state['time_arrival'].pop(0)
        
        # Calcula el retraso de este cliente y acumula
        delay = state['sim_time'] - arrival_time
        state['total_of_delays'] += delay
        state['num_custs_delayed'] += 1
        
        # Genera el tiempo de servicio y programa salida
        service_time = expon(mean_service)
        state['time_next_event'][2] = state['sim_time'] + service_time
        
        # Acumula tiempo en el sistema (retraso en cola + tiempo de servicio)
        state['total_time_in_system'] += delay + service_time



# ----------------- Función Principal de Simulación -----------------

# Cada cuántos clientes retrasados se captura un snapshot de métricas
HISTORY_INTERVAL = 100

def run_simulation(mean_interarrival, mean_service, num_delays_required, queue_limit, seed):
    # Inicializa el generador de números aleatorios para esta corrida
    random.seed(seed)
    
    # Inicializa el estado del sistema
    state = initialize(mean_interarrival)
    last_snapshot = 0  # Número de clientes retrasados en el último snapshot

    # Ciclo principal de simulación
    while state['num_custs_delayed'] < num_delays_required:
        # Determina el tipo del siguiente evento
        next_event_type = timing(state)
        
        if next_event_type is None:
            break  # Si no hay más eventos programados
            
        # Actualiza las estadísticas de áreas antes de alterar el estado del sistema
        update_time_avg_stats(state)
        
        # Ejecuta la rutina de evento correspondiente
        if next_event_type == 1:
            arrive(state, mean_interarrival, mean_service, queue_limit)
        elif next_event_type == 2:
            depart(state, mean_service)

        # Captura snapshot de métricas cada HISTORY_INTERVAL clientes retrasados
        nd = state['num_custs_delayed']
        if nd > 0 and nd - last_snapshot >= HISTORY_INTERVAL:
            t = state['sim_time']
            utilization = state['area_server_status'] / t
            L_q = state['area_num_in_q'] / t
            L   = L_q + utilization
            W_q = state['total_of_delays'] / nd
            W   = state['total_time_in_system'] / nd
            state['history'].append((t, L, L_q, W, W_q))
            last_snapshot = nd
            
    return state




# Calcula las medidas de rendimiento a partir del estado de la simulación actual
def calculate_metrics(state):
    sim_time = state['sim_time']
    num_delayed = state['num_custs_delayed']
    arrived = state['num_custs_arrived']
    blocked = state['num_custs_blocked']
    utilization = state['area_server_status'] / sim_time # Utilización del servidor
   
    L_q = state['area_num_in_q'] / sim_time # Promedio de clientes en cola (Lq)
    L = L_q + utilization # Promedio de clientes en el sistema (L)
   
    W_q = state['total_of_delays'] / num_delayed # Tiempo promedio en cola (Wq)
    W = state['total_time_in_system'] / num_delayed # Tiempo promedio en el sistema (W)
    
    prob_n_in_q = {}
    for n, time_spent in state['time_in_q_state'].items(): # Probabilidad de encontrar n clientes en cola
        prob_n_in_q[n] = time_spent / sim_time
    
    prob_blocking = blocked / arrived if arrived > 0 else 0.0 # Probabilidad de denegación de servicio (bloqueo)
    
    return {
        'L': L,
        'L_q': L_q,
        'W': W,
        'W_q': W_q,
        'utilization': utilization,
        'prob_n_in_q': prob_n_in_q,
        'prob_blocking': prob_blocking,
        'sim_time': sim_time,
        'arrived': arrived,
        'blocked': blocked,
        'num_delayed': num_delayed
    }



# Imprimir resultados
def print_report(metrics, queue_limit, file=None):
    out = file if file else None
    
    def print_both(text):
        print(text)
        if out:
            out.write(text + "\n")
            
    print_both("=" * 60)
    print_both(f"  REPORTE DE SIMULACIÓN - MODELO DE COLA M/M/1{'/' + str(queue_limit) if queue_limit != float('inf') else ''}")
    print_both("=" * 60)
    print_both(f"Parámetros de Entrada:")
    print_both(f"  Tiempo promedio entre arribos (1/lambda): {MEAN_INTERARRIVAL:.3f} minutos")
    print_both(f"  Tiempo promedio de servicio (1/mu):       {MEAN_SERVICE:.3f} minutos")
    print_both(f"  Clientes requeridos en simulación:        {NUM_DELAYS_REQUIRED}")
    print_both(f"  Límite de la cola (K):                    {queue_limit if queue_limit != float('inf') else 'Infinito (M/M/1)'}")
    print_both(f"  Semilla aleatoria:                        {RANDOM_SEED}")
    print_both("-" * 60)
    print_both(f"Medidas de Rendimiento:")
    print_both(f"  Tiempo de simulación transcurrido:        {metrics['sim_time']:.3f} minutos")
    print_both(f"  Clientes que iniciaron servicio:          {metrics['num_delayed']}")
    print_both(f"  Clientes arribados en total:              {metrics['arrived']}")
    print_both(f"  Clientes bloqueados:                      {metrics['blocked']}")
    print_both("-" * 60)
    print_both(f"  1. Promedio de clientes en el sistema (L): {metrics['L']:.4f}")
    print_both(f"  2. Promedio de clientes en cola (Lq):      {metrics['L_q']:.4f}")
    print_both(f"  3. Tiempo promedio en el sistema (W):      {metrics['W']:.4f} minutos")
    print_both(f"  4. Tiempo promedio en cola (Wq):           {metrics['W_q']:.4f} minutos")
    print_both(f"  5. Utilización del servidor (Rho):         {metrics['utilization']:.4f}")
    print_both(f"  6. Probabilidad de denegación de servicio: {metrics['prob_blocking']:.4f} ({metrics['prob_blocking']*100:.2f}%)")
    print_both("-" * 60)
    print_both("  7. Probabilidad de encontrar n clientes en cola (P(Nq = n)):")
    for n in sorted(metrics['prob_n_in_q'].keys()):
        p = metrics['prob_n_in_q'][n]
        print_both(f"     n = {n:2d}: Probabilidad = {p:.4f} ({p*100:5.2f}%)")
    print_both("=" * 60 + "\n")





# ----------------- Gráficos de evolución temporal -----------------
def plot_metrics(history, queue_limit):
    """
    Genera dos subgráficos con la evolución de las métricas de rendimiento
    a lo largo del tiempo de simulación:
      - Subplot 1: Promedio de clientes en cola (Lq) y en el sistema (L)
      - Subplot 2: Tiempo promedio en sistema (W) y en cola (Wq)
    """
    if not history:
        print("No hay datos de historial para graficar.")
        return

    times = [h[0] for h in history]
    L_vals  = [h[1] for h in history]
    Lq_vals = [h[2] for h in history]
    W_vals  = [h[3] for h in history]
    Wq_vals = [h[4] for h in history]

    title_suffix = f"M/M/1/{queue_limit}" if queue_limit != float('inf') else "M/M/1"

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    fig.suptitle(f"Evolución temporal de métricas — Modelo {title_suffix}", fontsize=13, fontweight='bold')

    # --- Subplot 1: L y Lq ---
    ax1.plot(times, Lq_vals, color='deeppink',  linewidth=1.5, label='Promedio de clientes en cola (Lq)')
    ax1.plot(times, L_vals,  color='dodgerblue', linewidth=1.5, label='Promedio de clientes en sistema (L)')
    ax1.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax1.set_ylabel('Clientes')
    ax1.legend(loc='upper right', fontsize=8)
    ax1.grid(True, linestyle='--', alpha=0.5)
    ax1.set_title('Clientes promedio en cola y en sistema')

    # --- Subplot 2: W y Wq ---
    ax2.plot(times, W_vals,  color='deeppink',  linewidth=1.5, label='Tiempo promedio en sistema (W)')
    ax2.plot(times, Wq_vals, color='orange',     linewidth=1.5, label='Tiempo promedio en cola (Wq)')
    ax2.axhline(0, color='gray', linewidth=0.5, linestyle='--')
    ax2.set_ylabel('Minutos')
    ax2.set_xlabel('Tiempo de simulación (minutos)')
    ax2.legend(loc='upper right', fontsize=8)
    ax2.grid(True, linestyle='--', alpha=0.5)
    ax2.set_title('Tiempos promedio en sistema y en cola')

    plt.tight_layout()
    plt.savefig('mm1_metricas_tiempo.png', dpi=150)
    plt.show()
    print("Gráfico guardado en 'mm1_metricas_tiempo.png'.")


# ------------- Simulación ------------- 
def main():
    # Simulación Principal
    print("Ejecutando simulación principal...")
    state_main = run_simulation(MEAN_INTERARRIVAL, MEAN_SERVICE, NUM_DELAYS_REQUIRED, QUEUE_LIMIT, RANDOM_SEED)
    metrics_main = calculate_metrics(state_main)
    
    # Escribir reporte en archivo mm1.out y mostrar por pantalla
    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        print_report(metrics_main, QUEUE_LIMIT, outfile)
        
    print(f"Reporte detallado guardado en '{OUTPUT_FILE}'.\n")
    
    # Simulación de Comparación (Denegación de servicio con cola finita de tamaño: 0, 2, 5, 10, 50)
    print("Ejecutando comparación de denegación de servicio para colas finitas K = [0, 2, 5, 10, 50]...")
    capacities = [0, 2, 5, 10, 50]
    comparison_results = []
    
    for cap in capacities:
        state_cap = run_simulation(MEAN_INTERARRIVAL, MEAN_SERVICE, NUM_DELAYS_REQUIRED, cap, RANDOM_SEED)
        metrics_cap = calculate_metrics(state_cap)
        comparison_results.append((cap, metrics_cap))
        
    # Tabla comparativa
    print("\n" + "=" * 80)
    print("  TABLA COMPARATIVA: EFECTO DEL TAMAÑO DE COLA (K) SOBRE LA DENEGACIÓN DE SERVICIO")
    print("=" * 80)
    print(f"  Parámetros: Interarribo={MEAN_INTERARRIVAL:.2f} min | Servicio={MEAN_SERVICE:.2f} min | Clientes={NUM_DELAYS_REQUIRED}")
    print("-" * 80)
    print(f" {'Cola (K)':<10} | {'Arribos':<10} | {'Bloqueados':<10} | {'P(Denegación)':<15} | {'Utilización':<12} | {'Lq':<8}")
    print("-" * 80)
    for cap, met in comparison_results:
        print(f" {cap:<10d} | {met['arrived']:<10d} | {met['blocked']:<10d} | {met['prob_blocking']:<15.6f} | {met['utilization']:<12.4f} | {met['L_q']:<8.4f}")
    print("=" * 80)
    
    # Archivo de salida
    with open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:
        outfile.write("\n" + "=" * 80 + "\n")
        outfile.write("  TABLA COMPARATIVA: EFECTO DEL TAMAÑO DE COLA (K) SOBRE LA DENEGACIÓN DE SERVICIO\n")
        outfile.write("=" * 80 + "\n")
        outfile.write(f"  Parámetros: Interarribo={MEAN_INTERARRIVAL:.2f} min | Servicio={MEAN_SERVICE:.2f} min | Clientes={NUM_DELAYS_REQUIRED}\n")
        outfile.write("-" * 80 + "\n")
        outfile.write(f"  {'Cola (K)':<10} | {'Arribos':<10} | {'Bloqueados':<10} | {'P(Denegación)':<15} | {'Utilización':<12} | {'Lq':<8}\n")
        outfile.write("-" * 80 + "\n")
        for cap, met in comparison_results:
            outfile.write(f"  {cap:<10d} | {met['arrived']:<10d} | {met['blocked']:<10d} | {met['prob_blocking']:<15.6f} | {met['utilization']:<12.4f} | {met['L_q']:<8.4f}\n")
        outfile.write("=" * 80 + "\n")

    # Gráfico de evolución temporal con la corrida principal
    print("\nGenerando gráficos de evolución temporal...")
    plot_metrics(state_main['history'], QUEUE_LIMIT)

if __name__ == '__main__':
    main()
