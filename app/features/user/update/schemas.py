# ============================================================================
# schemas.py — Modelos Pydantic para PUT /user/me (configuraciones)
# ============================================================================

from pydantic import BaseModel


class UserUpdateConfigRequest(BaseModel):
    """Datos para actualizar la configuración de un usuario."""
    telefono: str = ""
    nombre_empresa: str = ""
    shalom: bool = False
    marvisur: bool = False
    olva: bool = False
    retiro_tienda: bool = False
    dinsides: bool = False
    delivery: bool = False


class UserUpdateConfigResponse(BaseModel):
    """Respuesta del endpoint PUT /user/me."""
    success: bool
    message: str
