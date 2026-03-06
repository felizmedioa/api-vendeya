# ============================================================================
# routes.py — Endpoint de usuarios
# ============================================================================

from fastapi import APIRouter

from app.features.usuarios.service import get_user

router = APIRouter(
    tags=["Usuarios"],
)


@router.get(
    "/obtener-datos",
    summary="Obtener datos del usuario autenticado",
)
async def obtener_datos():
    return await get_user()
