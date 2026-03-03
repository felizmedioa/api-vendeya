from app.shared.http_client import ShalomHttpClient

async def eliminar_ordenes(client: ShalomHttpClient, id: int) -> dict:
    client.verificar_sesion()
    headers = client.obtener_headers_ajax()
    
    # IMPORTANTE: Reemplazar el url por el endpoint real proporcionado por el backend/Shalom
    response = await client.client.delete(
        f"/service-order/{id}", 
        headers=headers,
    )

    return response.status_code

