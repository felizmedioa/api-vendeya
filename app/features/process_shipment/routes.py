# ============================================================================
# routes.py — Endpoint combinado: filleo → preregister → register
# ============================================================================

from fastapi import APIRouter

from app.features.process_shipment.schemas import (
    ProcessShipmentRequest,
    ProcessShipmentResponse,
)
from app.features.process_shipment.service import procesar_envio

router = APIRouter(
    tags=["Procesar Envío"],
)


@router.post(
    "/procesar-envio",
    response_model=ProcessShipmentResponse,
    summary="Procesar envío completo",
    description=(
        "Ejecuta los 5 pasos del envío: login → filleo → preregister → "
        "set_code → register. Cada llamada usa su propio cliente HTTP "
        "independiente, permitiendo múltiples llamadas concurrentes."
    ),
)
async def procesar_envio_endpoint(
    datos: ProcessShipmentRequest,
):
    return await procesar_envio(datos)
