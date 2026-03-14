# ============================================================================
# service.py — Lógica de preregister
# ============================================================================

from app.features.process_shipment.preregister.schemas import SendRequest
from app.shared.http_client import HttpClient

async def obtener_envios(client: HttpClient, claves: SendRequest) -> dict:
    client.verificar_sesion()
    headers = client.obtener_headers_ajax()
    response = await client.client.post(
        "/envia_ya/envios",
        headers=headers,
        json = claves.model_dump()
    )
    return response.json()
