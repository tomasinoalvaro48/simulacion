import random
import math
import statistics


# PARÁMETROS DEL SISTEMA DE INVENTARIO
# =====================================

INITIAL_INV_LEVEL = 60 # Nivel de inventario inicial
NUM_MONTHS = 120 # Duración de la simulación en meses
MEAN_INTERDEMAND = 0.1 # Tiempo promedio entre demandas (meses) — proceso Poisson de llegadas
PROB_DISTRIB_DEMAND = [0.0, 1/6, 1/6 + 1/3, 1/6 + 1/3 + 1/3, 1.0] # Distribución acumulada del tamaño de la demanda (índices 1..4)
NUM_VALUES_DEMAND = 4 # Número de valores posibles de demanda
# Lag 
MINLAG = 0.5
MAXLAG = 1.0

# Costos
# Justificación: Valores canónicos del modelo de Law & Kelton.
#   K  = costo fijo de cada orden (setup cost)
#   i  = costo incremental por unidad ordenada
#   h  = costo de mantenimiento por unidad por mes
#   pi = costo de faltante por unidad por mes (> h para reflejar pérdida de ventas)
SETUP_COST = 32.0
INCREMENTAL_COST = 3.0
HOLDING_COST = 1.0
SHORTAGE_COST = 5.0

# Políticas (s, S) a evaluar
# s = punto de reorden (se pide si inv_level < s)
# S = nivel objetivo al que se repone (se pide S - inv_level unidades)
POLICIES = [
    (20,  40),
    (20,  60),
    (20,  80),
    (20, 100),
    (40,  60),
    (40,  80),
    (40, 100),
    (60,  80),
    (60, 100),
]

NUM_REPLICATIONS = 10 # Número mínimo de réplicas por política
OUTPUT_FILE = "inventario.out" # Archivo de salida
BASE_SEED = 42 # Semilla base



# FUNCIONES AUXILIARES DE GENERACIÓN DE VARIABLES ALEATORIAS
# ============================================================

def expon(mean):
    return random.expovariate(1.0 / mean)


def uniform(a, b):
    return random.uniform(a, b)


#Genera un entero aleatorio de acuerdo a la función de distribución acumulada `prob_distrib`
def random_integer(prob_distrib):
    u = random.random()
    for i in range(1, len(prob_distrib)):
        if u < prob_distrib[i]:
            return i
    return len(prob_distrib) - 1



# FUNCIONES DE INICIALIZACIÓN Y RUTINAS DE EVENTOS
# =================================================

def initialize(smalls, bigs):
    """
    Eventos:
        1 -> Llegada de orden (order arrival)
        2 -> Demanda del cliente
        3 -> Fin de simulación (end-of-simulation)
        4 -> Evaluación de inventario (mensual)
    """
    state = {
        'sim_time': 0.0,
        'inv_level': INITIAL_INV_LEVEL,
        'time_last_event': 0.0,
        'amount': 0,
        'smalls': smalls,
        'bigs': bigs,
        'total_ordering_cost': 0.0,
        'area_holding': 0.0,
        'area_shortage': 0.0,
        'time_next_event': {
            1: 1.0e+30, # Llegada de orden (ninguna pendiente)
            2: expon(MEAN_INTERDEMAND), # Primera demanda
            3: float(NUM_MONTHS), # Fin de simulación
            4: 0.0, # Primera evaluación (en t=0)
        }
    }
    return state


def timing(state):
    min_time = float('inf')
    next_event_type = 0

    for event_type, event_time in state['time_next_event'].items():
        if event_time < min_time:
            min_time = event_time
            next_event_type = event_type

    state['sim_time'] = min_time
    return next_event_type


def update_time_avg_stats(state):
    # Actualiza los acumuladores de área (integrales en el tiempo)
    time_since_last_event = state['sim_time'] - state['time_last_event']
    state['time_last_event'] = state['sim_time']

    if state['inv_level'] < 0:
        # Inventario negativo -> costo de faltante
        state['area_shortage'] -= state['inv_level'] * time_since_last_event
    elif state['inv_level'] > 0:
        # Inventario positivo -> costo de mantenimiento
        state['area_holding'] += state['inv_level'] * time_since_last_event


def order_arrival(state):
    # Evento 1: Llegada de una orden previamente realizada.
    # Incrementa el nivel de inventario y desactiva el evento de llegada.
    state['inv_level'] += state['amount']
    state['time_next_event'][1] = 1.0e+30


def demand(state):
    # Evento 2: Demanda de un cliente.
    # Decrementa el inventario según un tamaño de demanda aleatorio y programa la próxima demanda.
    state['inv_level'] -= random_integer(PROB_DISTRIB_DEMAND)
    state['time_next_event'][2] = state['sim_time'] + expon(MEAN_INTERDEMAND)


def evaluate(state):
    # Evento 4: Evaluación mensual del nivel de inventario (política (s,S)).
    # Si inv_level < s, se realiza un pedido de (S - inv_level) unidades.
    # Se programa la próxima evaluación un mes después.
    if state['inv_level'] < state['smalls']:
        state['amount'] = state['bigs'] - state['inv_level']
        state['total_ordering_cost'] += (
            SETUP_COST + INCREMENTAL_COST * state['amount']
        )
        state['time_next_event'][1] = state['sim_time'] + uniform(MINLAG, MAXLAG)

    state['time_next_event'][4] = state['sim_time'] + 1.0


def calculate_metrics(state):
    # Calcula las métricas de rendimiento al finalizar la réplica.
    # Devuelve costos promedio mensuales.
    avg_ordering_cost = state['total_ordering_cost'] / NUM_MONTHS
    avg_holding_cost  = HOLDING_COST  * state['area_holding']  / NUM_MONTHS
    avg_shortage_cost = SHORTAGE_COST * state['area_shortage']  / NUM_MONTHS
    avg_total_cost    = avg_ordering_cost + avg_holding_cost + avg_shortage_cost

    return {
        'ordering_cost': avg_ordering_cost,
        'holding_cost':  avg_holding_cost,
        'shortage_cost': avg_shortage_cost,
        'total_cost':    avg_total_cost,
    }



# FUNCIÓN PRINCIPAL DE SIMULACIÓN (UNA RÉPLICA)
# ==============================================

def run_simulation(smalls, bigs, seed):
    random.seed(seed)
    state = initialize(smalls, bigs)

    while True:
        next_event_type = timing(state)
        update_time_avg_stats(state)

        if next_event_type == 1:
            order_arrival(state)
        elif next_event_type == 2:
            demand(state)
        elif next_event_type == 4:
            evaluate(state)
        elif next_event_type == 3:
            break # Fin de la simulación para esta réplica

    return calculate_metrics(state)



# FUNCIÓN DE EXPERIMENTO (MÚLTIPLES RÉPLICAS)
# ============================================

def run_experiment(smalls, bigs, num_replications, base_seed):
    # Ejecuta `num_replications` réplicas independientes para la política (s, S)
    # y agrega los resultados. Devuelve promedios y desviaciones estándar.
    results = {
        'ordering_cost': [],
        'holding_cost':  [],
        'shortage_cost': [],
        'total_cost':    [],
    }

    for rep in range(num_replications):
        metrics = run_simulation(smalls, bigs, base_seed + rep)
        for key in results:
            results[key].append(metrics[key])

    aggregated = {}
    for key, values in results.items():
        aggregated[f'{key}_mean'] = statistics.mean(values)
        aggregated[f'{key}_std']  = statistics.stdev(values) if len(values) > 1 else 0.0
        aggregated[f'{key}_runs'] = values

    return aggregated



# GENERACIÓN DE REPORTE
# ======================

def print_header(file=None):
    """Imprime los encabezados del reporte con los parámetros del experimento."""
    prob_str = "  ".join(f"{p:.4f}" for p in PROB_DISTRIB_DEMAND[1:])
    lines = [
        "=" * 80,
        "  SIMULACION DE SISTEMA DE INVENTARIO -- MODELO (s, S)",
        "=" * 80,
        f"  Nivel inicial de inventario : {INITIAL_INV_LEVEL} unidades",
        f"  Duracion de la simulacion   : {NUM_MONTHS} meses",
        f"  Nro. de valores de demanda  : {NUM_VALUES_DEMAND}",
        f"  Distribucion acumulada (F)  : {prob_str}",
        f"  Tiempo promedio entre demand: {MEAN_INTERDEMAND:.2f} meses",
        f"  Rango de tiempo de entrega  : [{MINLAG:.2f}, {MAXLAG:.2f}] meses",
        f"  Costos -> K={SETUP_COST:.1f}  i={INCREMENTAL_COST:.1f}  h={HOLDING_COST:.1f}  pi={SHORTAGE_COST:.1f}",
        f"  Replicas por politica       : {NUM_REPLICATIONS}",
        f"  Semilla base                : {BASE_SEED}",
        "=" * 80,
    ]
    for line in lines:
        print(line)
        if file:
            file.write(line + "\n")


def print_policy_detail(smalls, bigs, agg, file=None):
    """Imprime el detalle de cada réplica para una política (s, S)."""
    def w(text):
        print(text)
        if file:
            file.write(text + "\n")

    w(f"\n  Politica ({smalls:3d}, {bigs:3d})")
    w(f"  {'Replica':<10} {'C. Orden':>14} {'C. Manten.':>14} {'C. Faltante':>14} {'C. Total':>14}")
    w("  " + "-" * 58)
    for i, (o, h, s, t) in enumerate(zip(
            agg['ordering_cost_runs'],
            agg['holding_cost_runs'],
            agg['shortage_cost_runs'],
            agg['total_cost_runs']), start=1):
        w(f"  {i:<10d} {o:>14.4f} {h:>14.4f} {s:>14.4f} {t:>14.4f}")

    w("  " + "-" * 58)
    w(f"  {'Promedio':<10} "
      f"{agg['ordering_cost_mean']:>14.4f} "
      f"{agg['holding_cost_mean']:>14.4f} "
      f"{agg['shortage_cost_mean']:>14.4f} "
      f"{agg['total_cost_mean']:>14.4f}")
    w(f"  {'Desv. Std':<10} "
      f"{agg['ordering_cost_std']:>14.4f} "
      f"{agg['holding_cost_std']:>14.4f} "
      f"{agg['shortage_cost_std']:>14.4f} "
      f"{agg['total_cost_std']:>14.4f}")


def print_summary_table(all_results, file=None):
    """Imprime la tabla resumen comparando todas las políticas."""
    def w(text):
        print(text)
        if file:
            file.write(text + "\n")

    w("\n" + "=" * 80)
    w("  TABLA RESUMEN COMPARATIVA DE POLITICAS (promedios sobre replicas)")
    w("=" * 80)
    w(f"  {'Politica':<12} {'C. Orden':>14} {'C. Manten.':>14} {'C. Faltante':>14} {'C. Total':>14}")
    w("  " + "-" * 72)

    best_policy = None
    best_cost   = float('inf')

    for (s, S), agg in all_results:
        label = f"({s:3d},{S:3d})"
        w(f"  {label:<12} "
          f"{agg['ordering_cost_mean']:>14.4f} "
          f"{agg['holding_cost_mean']:>14.4f} "
          f"{agg['shortage_cost_mean']:>14.4f} "
          f"{agg['total_cost_mean']:>14.4f}")
        if agg['total_cost_mean'] < best_cost:
            best_cost   = agg['total_cost_mean']
            best_policy = (s, S)

    w("  " + "=" * 72)
    w(f"\n  * Politica optima: ({best_policy[0]}, {best_policy[1]})"
      f"  -- Costo total promedio: {best_cost:.4f} $/mes")
    w("=" * 80 + "\n")







def main():
    all_results = []

    with open(OUTPUT_FILE, "w", encoding="utf-8") as outfile:
        print_header(outfile)

        for smalls, bigs in POLICIES:
            agg = run_experiment(smalls, bigs, NUM_REPLICATIONS, BASE_SEED)
            all_results.append(((smalls, bigs), agg))
            print_policy_detail(smalls, bigs, agg, outfile)

        print_summary_table(all_results, outfile)

    print(f"\nReporte detallado guardado en '{OUTPUT_FILE}'.")


if __name__ == '__main__':
    main()
