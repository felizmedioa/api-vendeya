# ============================================================================
# schemas.py — Modelos Pydantic para el proceso combinado de envío
# ============================================================================

from pydantic import BaseModel


class ProcessShipmentRequest(BaseModel):
    """Datos necesarios para procesar un envío completo (filleo + preregister + register)."""
    dni: str
    telefono: str
    destino: str


class ProcessShipmentResponse(BaseModel):
    """Respuesta del proceso combinado de envío."""
    success: bool
    failed_step: str | None = None
    order_id: int | None = None
    detail: str
