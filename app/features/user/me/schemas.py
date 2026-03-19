# ============================================================================
# schemas.py — Modelos Pydantic para GET /user/me (configuraciones)
# ============================================================================

from pydantic import BaseModel
from typing import Optional


class UserConfig(BaseModel):
    """Datos de configuración de un usuario obtenidos desde Google Sheet."""
    id: str
    shalom: bool = False
    marvisur: bool = False
    delivery: bool = False
    dinsides: bool = False
    olva: bool = False
    retiro_tienda: bool = False
    create_config: bool = False
    telefono: str = ""
    nombre_empresa: str = ""


class UserConfigResponse(BaseModel):
    """Respuesta del endpoint GET /user/me."""
    success: bool
    message: str
    config: Optional[UserConfig] = None
