from app.features.set_code.schemas import SetCodeRequest, SetCodeResponse
from app.shared.http_client import ShalomHttpClient

async def set_code(client: ShalomHttpClient, datos: SetCodeRequest) -> SetCodeResponse:

    client.verificar_sesion()
    headers = client.obtener_headers_ajax()

    response = await client.client.post(
        "/security-code/massive",
        headers=headers,
        json=datos.dict(),
    )

    return response.json()
    