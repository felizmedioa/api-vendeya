# ============================================================================
# routes.py — Endpoint de búsqueda
# ============================================================================

from fastapi import APIRouter

from app.features.search.schemas import BusquedaRequest, BusquedaResponse
from app.features.search.service import buscar

router = APIRouter(
    tags=["Búsqueda"],
)


@router.post(
    "/buscar-persona",
    response_model=BusquedaResponse,
    summary="Buscar según datos del formulario",
    description="Busca en Shalom usando tipo de producto, origen y destino.",
)
async def buscar_endpoint(
    datos: BusquedaRequest,
):
    return await buscar(datos)
