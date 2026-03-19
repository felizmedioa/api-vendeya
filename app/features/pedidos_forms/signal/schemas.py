from pydantic import BaseModel, Field
from typing import List

class PedidoStatusUpdate(BaseModel):
    pedidos_ids: List[str] = Field(..., description="Lista de IDs de pedidos a actualizar")
    nuevo_estado: str = Field(default="Impreso", description="Estado nuevo a asignar (ej. Impreso)")
