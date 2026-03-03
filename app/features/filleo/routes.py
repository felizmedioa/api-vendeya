# ============================================================================
# routes.py — Endpoint de filleo
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.filleo.schemas import FilleoRequest, FilleoResponse
from app.features.filleo.service import fillear, fill_book
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Filleo"],
)


@router.post(
    "/filleo",
    # response_model=FilleoResponse,
    summary="Ejecutar filleo",
    description="Envía datos de filleo a Shalom. Requiere sesión activa.",
)
async def filleo_endpoint(
    datos: FilleoRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    ruta = fill_book('formato-envio.xlsx', datos)
    return await fillear(client, ruta)
