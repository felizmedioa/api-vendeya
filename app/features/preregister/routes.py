# ============================================================================
# routes.py — Endpoint de búsqueda
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.shared.http_client import ShalomHttpClient
from app.features.preregister.service import obtener_envios
from app.features.preregister.schemas import SendRequest

router = APIRouter(
    tags=["Registro de envios"],
)

@router.post(
    "/obtener-preenvios",
    summary="Obtener preenvios",
    description="Obtiene los preenvios",
)
async def obtener_preenvios(
    claves: SendRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    response = await obtener_envios(client, claves)
    
    return response