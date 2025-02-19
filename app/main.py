from fastapi import FastAPI, HTTPException
from models import TransportProblem, TransportSolution
from solver import solve_transport_problem

app = FastAPI(
    title="API de Optimización de Transporte",
    description="API para resolver problemas de optimización de transporte usando el método simplex",
    version="1.0.0"
)

@app.post(
    "/solve",
    response_model=TransportSolution,
    summary="Resolver problema de transporte",
    description="Resuelve un problema de optimización de transporte y verifica su optimalidad",
    response_description="Retorna la matriz de solución, el costo óptimo y si la solución es óptima"
)
async def solve(
    problem: TransportProblem = {
        "costs": [
            [5, 2, 7, 3],
            [3, 5, 6, 1],
            [6, 1, 2, 4],
            [4, 3, 6, 6]
        ],
        "supply": [80, 30, 60, 45],
        "demand": [70, 40, 70, 35]
    }
):
    """
    Resuelve un problema de transporte con los siguientes parámetros:
    
    - **costs**: Matriz de costos donde costs[i][j] es el costo de transportar desde el origen i al destino j
    - **supply**: Lista de capacidades de suministro de cada origen
    - **demand**: Lista de demandas de cada destino
    
    Retorna:
    - **solution**: Matriz con los costos reducidos
    - **optimal_cost**: Costo total mínimo de la solución
    - **is_optimal**: Boolean que indica si la solución es óptima
    """
    try:
        result = solve_transport_problem(
            problem.costs,
            problem.supply,
            problem.demand
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Bienvenido a la API de Optimización de Transporte. Accede a /docs para ver la documentación."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
