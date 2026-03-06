from app.shared.http_client import ShalomHttpClient
from app.features.process_shipment.auth.service import login

async def eliminar_ordenes(id: int) -> dict:
    """
    Elimina una orden de servicio.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = ShalomHttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()
        
        response = await client.client.delete(
            f"/service-order/{id}", 
            headers=headers,
        )

        return response.status_code
    finally:
        await client.close()
