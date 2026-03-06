# ============================================================================
# service.py — Lógica de productos con Shalom
# ============================================================================

from app.shared.http_client import ShalomHttpClient
from app.features.process_shipment.auth.service import login


async def get_productos() -> dict:
    """
    Obtiene la lista de productos de Envía Ya.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = ShalomHttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()
        response = await client.client.post("/envia_ya/products", headers=headers)
        return response.json()
    finally:
        await client.close()