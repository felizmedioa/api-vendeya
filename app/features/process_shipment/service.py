# ============================================================================
# service.py — Orquestación: login → filleo → preregister → set_code → register
# ============================================================================
# Cada llamada crea su propio HttpClient con sesión independiente.
# Esto permite múltiples llamadas concurrentes sin interferencia.
# ============================================================================

import logging

from app.features.process_shipment.auth.service import login
from app.features.process_shipment.filleo.schemas import FilleoRequest
from app.features.process_shipment.filleo.service import fill_book, fillear
from app.features.process_shipment.preregister.schemas import SendRequest
from app.features.process_shipment.preregister.service import obtener_envios
from app.features.process_shipment.register.schemas import RegisterRequest
from app.features.process_shipment.register.service import registrar_orden
from app.features.process_shipment.schemas import (
    ProcessShipmentRequest,
    ProcessShipmentResponse,
)
from app.shared.http_client import HttpClient
from app.features.process_shipment.set_code.service import set_code
from app.features.process_shipment.set_code.schemas import SetCodeRequest

from app.core.config import settings

logger = logging.getLogger("process_shipment")


async def procesar_envio(
    datos: ProcessShipmentRequest,
) -> ProcessShipmentResponse:
    """
    Ejecuta secuencialmente los 5 pasos del flujo de envío,
    cada uno con su propio cliente HTTP independiente.

    0. Login      – crea cliente, inicia sesión y obtiene cookies.
    1. Filleo     – llena el Excel y lo sube.
    2. Preregister – obtiene los pre-envíos y extrae el id.
    3. Set Code   – asigna el código a los envíos.
    4. Register   – registra la orden con el id obtenido.

    Si cualquier paso falla, retorna inmediatamente indicando
    cuál fue el paso que falló. El cliente se cierra siempre al final.
    """

    client = HttpClient()

    try:
        # ── Paso 0: Login ────────────────────────────────────────────────
        
        try:
            await login(client)
            
        except Exception as exc:

            return ProcessShipmentResponse(
                success=False,
                failed_step="login",
                detail=f"Error en login: {exc}",
            )

        # ── Paso 1: Filleo ───────────────────────────────────────────────
        
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

        # ── Paso 2: Preregister ──────────────────────────────────────────
        
        try:
            preregister_request = SendRequest(converted=False, send=False)
            response = await obtener_envios(client, preregister_request)
            print(response)
            order_id: int = response["data"][0]["id"]
            
        except Exception as exc:
            
            return ProcessShipmentResponse(
                success=False,
                failed_step="preregister",
                detail=f"Error en preregister: {exc}",
            )

        # ── Paso 3: Set Code ────────────────────────────────────────────
        
        try:
            set_code_request = SetCodeRequest(code=settings.CLAVE_PAQUETE)
            await set_code(client, set_code_request)
            
        except Exception as exc:
            
            return ProcessShipmentResponse(
                success=False,
                failed_step="set_code",
                detail=f"Error en set_code: {exc}",
            )

        # ── Paso 4: Register ────────────────────────────────────────────
        
        try:
            register_request = RegisterRequest(serviceOrder=[order_id])
            resultado = await registrar_orden(client, register_request)
            
        except Exception as exc:
            
            return ProcessShipmentResponse(
                success=False,
                failed_step="register",
                detail=f"Error en register: {exc}",
            )

        # ── Todo bien ────────────────────────────────────────────────────
        
        return ProcessShipmentResponse(
            success=True,
            order_id=order_id,
            detail=f"Envío procesado correctamente. Resultado: {resultado}",
        )

    finally:
        # Siempre cerrar el cliente, haya éxito o error
        await client.close()
