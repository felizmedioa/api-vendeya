# ============================================================================
# service.py — Lógica de búsqueda con Shalom
# ============================================================================

from app.features.preregister.schemas import SendRequest
from app.shared.http_client import ShalomHttpClient

async def obtener_envios(client: ShalomHttpClient, claves: SendRequest) -> dict:
    client.verificar_sesion()
    headers = client.obtener_headers_ajax()
    response = await client.client.post(
        "/envia_ya/envios",
        headers=headers,
        json = claves.model_dump()
    )
    return response.json()