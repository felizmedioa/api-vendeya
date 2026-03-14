# ============================================================================
# routes.py — Endpoints de usuario
# ============================================================================

from fastapi import APIRouter

from app.features.user.schemas import UserResponse, UserUpdateRequest
from app.features.user.service import get_current_user, update_user

router = APIRouter(
    prefix="/user",
    tags=["User"],
)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Obtener usuario actual",
    description="Retorna los datos del usuario autenticado.",
)
async def get_me_endpoint():
    return await get_current_user()


@router.put(
    "/me",
    response_model=UserResponse,
    summary="Actualizar usuario actual",
    description="Actualiza los datos del usuario autenticado.",
)
async def update_me_endpoint(datos: UserUpdateRequest):
    return await update_user(datos)
