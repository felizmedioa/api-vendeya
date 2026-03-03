# ============================================================================
# routes.py — Endpoint combinado: filleo → preregister → register
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.process_shipment.schemas import (
    ProcessShipmentRequest,
    ProcessShipmentResponse,
)
from app.features.process_shipment.service import procesar_envio
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Procesar Envío"],
)


@router.post(
    "/procesar-envio",
    response_model=ProcessShipmentResponse,
    summary="Procesar envío completo",
    description=(
        "Ejecuta secuencialmente filleo → preregister → register. "
        "Retorna si el proceso fue exitoso o en qué paso falló."
    ),
)
async def procesar_envio_endpoint(
    datos: ProcessShipmentRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await procesar_envio(client, datos)
