# ============================================================================
# schemas.py — Modelos Pydantic compartidos del feature auth
# ============================================================================

from pydantic import BaseModel


class AuthResponse(BaseModel):
    """Respuesta genérica del feature de autenticación."""
    success: bool
    message: str
    data: dict | None = None
