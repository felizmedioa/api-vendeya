# ============================================================================
# schemas.py — Modelos Pydantic compartidos del feature user
# ============================================================================
# Los schemas específicos de cada sub-feature están en sus propias carpetas.
# Este archivo se usa para schemas compartidos entre sub-features.
# ============================================================================

from pydantic import BaseModel
from typing import Optional


class UserBase(BaseModel):
    """Datos base de un usuario (compartido entre sub-features)."""
    id: str | None = None
    name: str | None = None
    email: str | None = None
