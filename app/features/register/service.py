from app.features.register.schemas import RegisterRequest
from app.shared.http_client import ShalomHttpClient

async def registrar_orden(client: ShalomHttpClient, claves: RegisterRequest) -> dict:
    client.verificar_sesion()
    headers = client.obtener_headers_ajax()
    
    # IMPORTANTE: Reemplazar el url por el endpoint real proporcionado por el backend/Shalom
    response = await client.client.post(
        "/send-shalom", 
        headers=headers,
        json=claves.model_dump()
    )
    return response.json()
