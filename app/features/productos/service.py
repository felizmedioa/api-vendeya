# ============================================================================
# service.py — Lógica de productos con Shalom
# ============================================================================

from app.shared.http_client import ShalomHttpClient


async def get_productos(shalom: ShalomHttpClient) -> dict:
    """
    Obtiene la lista de productos de Envía Ya.

    ¿Por qué es POST y no GET?
    Porque así lo definió Shalom en su API interna.
    """
    shalom.verificar_sesion()
    headers = shalom.obtener_headers_ajax()
    response = await shalom.client.post("/envia_ya/products", headers=headers)
    return response.json()