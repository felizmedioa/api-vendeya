# ============================================================================
# schemas.py — Modelos Pydantic compartidos entre features
# ============================================================================

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Estructura estándar de error (para documentación en Swagger)."""
    detail: str
