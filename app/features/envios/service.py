# ============================================================================
# service.py — Lógica de envíos con Shalom
# ============================================================================

from app.shared.http_client import ShalomHttpClient
from app.features.process_shipment.auth.service import login


async def crear_envio(datos_envio: dict) -> dict:
    """
    Crea una orden de servicio (envío) en Shalom.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = ShalomHttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()
        response = await client.client.post(
            "/envia_ya/service_order/save",
            headers=headers,
            json=datos_envio,
        )
        return response.json()
    finally:
        await client.close()
