# ============================================================================
# schemas.py — Modelos Pydantic para autenticación
# ============================================================================

from pydantic import BaseModel


class LoginResponse(BaseModel):
    """Respuesta del endpoint de login."""
    estado: str
    mensaje: str
    xsrf_token: str
