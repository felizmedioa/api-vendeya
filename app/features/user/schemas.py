# ============================================================================
# schemas.py — Modelos Pydantic para el feature user
# ============================================================================

from pydantic import BaseModel
from typing import Optional


class UserResponse(BaseModel):
    """Datos de un usuario."""
    id: int | None = None
    name: str
    email: str
    phone: Optional[str] = None


class UserUpdateRequest(BaseModel):
    """Datos para actualizar un usuario."""
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
