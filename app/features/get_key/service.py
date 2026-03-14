from app.shared.http_client import HttpClient
from app.features.get_key.schemas import SetKeyRequest
from app.features.process_shipment.auth.service import login
from app.core.config import settings

async def obtener_clave_envio(id_envio: int):
    """
    Obtiene la clave de un envío.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = HttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()

        response = await client.client.post(
            "/api/get-send-code",
            headers=headers,
            json={"idose": id_envio},
        )
        return response.json()
    finally:
        await client.close()

async def asignar_clave(datos: SetKeyRequest):
    """
    Asigna una clave a un envío.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = HttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()

        response = await client.client.post(
            "/api/send-code",
            headers=headers,
            json=datos.model_dump(),
        )
        return response.json()
    finally:
        await client.close()