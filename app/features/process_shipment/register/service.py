# ============================================================================
# service.py — Lógica de register
# ============================================================================

from app.features.process_shipment.register.schemas import RegisterRequest
from app.shared.http_client import HttpClient

async def registrar_orden(client: HttpClient, claves: RegisterRequest) -> dict:
    client.verificar_sesion()
    headers = client.obtener_headers_ajax()
    
    response = await client.client.post(
        "/send-shalom", 
        headers=headers,
        json=claves.model_dump()
    )
    return response.json()
