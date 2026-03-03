# ============================================================================
# routes.py — Endpoint de búsqueda
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.search.schemas import BusquedaRequest, BusquedaResponse
from app.features.search.service import buscar
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Búsqueda"],
)


@router.post(
    "/buscar-persona",
    response_model=BusquedaResponse,
    summary="Buscar según datos del formulario",
    description="Busca en Shalom usando tipo de producto, origen y destino. Requiere sesión activa.",
)
async def buscar_endpoint(
    datos: BusquedaRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await buscar(client, datos)
