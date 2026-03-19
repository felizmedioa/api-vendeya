from pydantic import BaseModel, Field

class PedidoFormCreate(BaseModel):
    id_usuario: str = Field(..., description="ID del cliente que generó este formulario")
    agencia: str
    nombre_completo: str
    dni: str
    telefono: str
    destino: str
    direccion: str

class PedidoFormResponse(PedidoFormCreate):
    id_pedido: str
    estado: str
    fecha: str
    timestamp: str
