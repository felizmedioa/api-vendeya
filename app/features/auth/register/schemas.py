# ============================================================================
# schemas.py — Modelos Pydantic para registro de usuario
# ============================================================================

from pydantic import BaseModel


class RegisterRequest(BaseModel):
    """Datos necesarios para registrar un nuevo usuario."""
    user: str
    password: str



class RegisterResponse(BaseModel):
    """Respuesta del proceso de registro."""
    success: bool
    message: str
    token: str | None = None
