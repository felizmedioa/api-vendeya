# ============================================================================
# routes.py — Endpoint de usuarios
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.usuarios.service import get_user
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Usuarios"],
)


@router.get(
    "/obtener-datos",
    summary="Obtener datos del usuario autenticado",
    description="Requiere haber llamado primero a /obtener-token.",
)
async def obtener_datos(
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await get_user(client)
