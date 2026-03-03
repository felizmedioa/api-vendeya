# ============================================================================
# routes.py — Endpoint de autenticación
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.auth.schemas import LoginResponse
from app.features.auth.service import login
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Autenticación"],
)


@router.get(
    "/obtener-token",
    response_model=LoginResponse,
    summary="Iniciar sesión en Shalom",
    description="Obtiene el token CSRF, envía las credenciales y guarda las cookies de sesión.",
)
async def get_token_login(
    client: ShalomHttpClient = Depends(get_shalom_client),
):

    return await login(client)
