# ============================================================================
# service.py — Lógica de set_code
# ============================================================================

from app.features.process_shipment.set_code.schemas import SetCodeRequest
from app.shared.http_client import ShalomHttpClient

async def set_code(client: ShalomHttpClient, datos: SetCodeRequest):

    client.verificar_sesion()
    headers = client.obtener_headers_ajax()

    response = await client.client.post(
        "/security-code/massive",
        headers=headers,
        json=datos.model_dump(),
    )

    return response.json()
