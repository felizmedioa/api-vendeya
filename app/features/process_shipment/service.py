# ============================================================================
# service.py — Orquestación: filleo → preregister → register
# ============================================================================

from app.features.filleo.schemas import FilleoRequest
from app.features.filleo.service import fill_book, fillear
from app.features.preregister.schemas import SendRequest
from app.features.preregister.service import obtener_envios
from app.features.register.schemas import RegisterRequest
from app.features.register.service import registrar_orden
from app.features.process_shipment.schemas import (
    ProcessShipmentRequest,
    ProcessShipmentResponse,
)
from app.shared.http_client import ShalomHttpClient


async def procesar_envio(
    client: ShalomHttpClient,
    datos: ProcessShipmentRequest,
) -> ProcessShipmentResponse:
    """
    Ejecuta secuencialmente los 3 pasos del flujo de envío.

    1. Filleo  – llena el Excel y lo sube a Shalom.
    2. Preregister – obtiene los pre-envíos y extrae el id.
    3. Register – registra la orden con el id obtenido.

    Si cualquier paso falla, retorna inmediatamente indicando
    cuál fue el paso que falló.
    """

    # ── Paso 1: Filleo ──────────────────────────────────────────────────
    try:
        filleo_request = FilleoRequest(
            dni=datos.dni,
            telefono=datos.telefono,
            destino=datos.destino,
        )
        ruta = fill_book("formato-envio.xlsx", filleo_request)
        await fillear(client, ruta)
    except Exception as exc:
        return ProcessShipmentResponse(
            success=False,
            failed_step="filleo",
            detail=f"Error en filleo: {exc}",
        )

    # ── Paso 2: Preregister ──────────────────────────────────────────────
    try:
        preregister_request = SendRequest(converted=False, send=False)
        response = await obtener_envios(client, preregister_request)
        order_id: int = response["data"][0]["id"]
    except Exception as exc:
        return ProcessShipmentResponse(
            success=False,
            failed_step="preregister",
            detail=f"Error en preregister: {exc}",
        )

    # ── Paso 3: Register ────────────────────────────────────────────────
    try:
        register_request = RegisterRequest(serviceOrder=[order_id])
        resultado = await registrar_orden(client, register_request)
    except Exception as exc:
        return ProcessShipmentResponse(
            success=False,
            failed_step="register",
            detail=f"Error en register: {exc}",
        )

    # ── Todo bien ────────────────────────────────────────────────────────
    return ProcessShipmentResponse(
        success=True,
        order_id=order_id,
        detail=f"Envío procesado correctamente. Resultado: {resultado}",
    )
