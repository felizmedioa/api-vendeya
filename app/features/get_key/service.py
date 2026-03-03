from app.shared.http_client import ShalomHttpClient
from app.features.get_key.schemas import SetKeyRequest
from app.core.config import settings

async def obtener_clave_envio(shalom: ShalomHttpClient, id_envio: int):
    shalom.verificar_sesion()
    headers = shalom.obtener_headers_ajax()

    response = await shalom.client.post(
        "/api/get-send-code",
        headers=headers,
        json={"idose": id_envio},
    )
    return response.json()

async def asignar_clave(shalom: ShalomHttpClient, datos: SetKeyRequest):
    shalom.verificar_sesion()
    headers = shalom.obtener_headers_ajax()

    response = await shalom.client.post(
        "/api/send-code",
        headers=headers,
        json=datos.model_dump(),
    )
    return response.json()
    
    