# ============================================================================
# schemas.py — Modelos Pydantic para búsqueda
# ============================================================================

from pydantic import BaseModel
from typing import Optional


class BusquedaRequest(BaseModel):
    """Datos que llegan del formulario de búsqueda."""
    documento: str
    type: str

class EntidadData(BaseModel):
    """Datos de la entidad."""
    type_document: str
    document: str
    name: str
    lastname: str
    surname: str
    full_name: str
    phone: int
    email: Optional[str] = None
    address: Optional[str] = None
    


class BusquedaResponse(BaseModel):
    """Respuesta de la búsqueda."""
    success: bool
    message: str
    data: EntidadData
