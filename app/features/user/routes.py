# ============================================================================
# routes.py — Endpoints de usuario
# ============================================================================

from fastapi import APIRouter

from app.features.user.me.schemas import UserConfigResponse
from app.features.user.me.service import get_user_config

from app.features.user.update.schemas import (
    UserUpdateConfigResponse,
    UserUpdateConfigRequest,
)
from app.features.user.update.service import update_user_config

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get(
    "/me",
    response_model=UserConfigResponse,
    summary="Obtener configuraciones del usuario",
    description="Valida el JWT, extrae el user_id y retorna las configuraciones del usuario desde Google Sheet.",
)
async def get_me_endpoint(token: str):
    return await get_user_config(token)


@router.put(
    "/me",
    response_model=UserUpdateConfigResponse,
    summary="Actualizar configuraciones del usuario",
    description="Actualiza las preferencias de courier, teléfono y nombre de empresa en el Google Sheet.",
)
async def update_me_endpoint(datos: UserUpdateConfigRequest, token: str):
    return await update_user_config(token, datos)
