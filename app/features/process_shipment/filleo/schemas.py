# ============================================================================
# schemas.py — Modelos Pydantic para filleo
# ============================================================================

from pydantic import BaseModel


class FilleoRequest(BaseModel):
    dni: str
    telefono: str
    destino: str
