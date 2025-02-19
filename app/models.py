from pydantic import BaseModel, Field
from typing import List

class TransportProblem(BaseModel):
    costs: List[List[float]] = Field(..., description="Matriz de costos de transporte")
    supply: List[float] = Field(..., description="Lista de capacidades de suministro")
    demand: List[float] = Field(..., description="Lista de demandas")

class TransportSolution(BaseModel):
    solution: List[List[float]] = Field(..., description="Matriz de costos reducidos")
    optimal_cost: float = Field(..., description="Costo total mínimo")
    is_optimal: bool = Field(..., description="Indica si la solución es óptima")
