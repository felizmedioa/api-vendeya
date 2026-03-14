# ============================================================================
# schemas.py — Modelos Pydantic para login
# ============================================================================

from pydantic import BaseModel


class LoginRequest(BaseModel):
    """Datos para iniciar sesión. Puede ser con credenciales o con token JWT."""
    user: str | None = None
    password: str | None = None
    token: str | None = None


class LoginResponse(BaseModel):
    """Respuesta del proceso de login."""
    success: bool
    message: str
    token: str | None = None
