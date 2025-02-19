import numpy as np
from scipy.optimize import linprog

def check_optimality(solution, costs, supply, demand):
    """Verifica si la solución es óptima"""
    # Verifica restricciones de oferta
    supply_satisfied = all(
        abs(sum(row) - s) < 1e-10 
        for row, s in zip(solution, supply)
    )
    
    # Verifica restricciones de demanda
    demand_satisfied = all(
        abs(sum(solution[:, j]) - d) < 1e-10 
        for j, d in enumerate(demand)
    )
    
    # Verifica no negatividad
    non_negative = np.all(np.array(solution) >= -1e-10)
    
    # Verifica si el costo es mínimo (usando las condiciones de complementariedad)
    reduced_costs = np.array(costs)
    is_minimal = np.all(reduced_costs[solution > 0] >= -1e-10)
    
    return supply_satisfied and demand_satisfied and non_negative and is_minimal

def solve_transport_problem(costs: list, supply: list, demand: list):
    costs_array = np.array(costs).flatten()
    supply_array = np.array(supply)
    demand_array = np.array(demand)

    num_supply = len(supply_array)
    num_demand = len(demand_array)

    # Construir restricciones
    A_eq = []
    b_eq = []

    # Restricciones de oferta
    for i in range(num_supply):
        row = [0] * (num_supply * num_demand)
        for j in range(num_demand):
            row[i * num_demand + j] = 1
        A_eq.append(row)
        b_eq.append(supply_array[i])

    # Restricciones de demanda
    for j in range(num_demand):
        row = [0] * (num_supply * num_demand)
        for i in range(num_supply):
            row[i * num_demand + j] = 1
        A_eq.append(row)
        b_eq.append(demand_array[j])

    # Resolver
    result = linprog(costs_array, A_eq=A_eq, b_eq=b_eq, method='highs')

    if result.success:
        solution = np.array(result.x).reshape(num_supply, num_demand)
        is_optimal = check_optimality(solution, costs, supply_array, demand_array)
        return {
            "solution": solution.tolist(),
            "optimal_cost": float(result.fun),
            "is_optimal": is_optimal
        }
    else:
        raise ValueError("No se pudo encontrar una solución óptima")
