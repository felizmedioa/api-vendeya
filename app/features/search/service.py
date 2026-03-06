# ============================================================================
# service.py — Lógica de búsqueda con Shalom
# ============================================================================

from app.features.search.schemas import BusquedaRequest, BusquedaResponse
from app.shared.http_client import ShalomHttpClient
from app.features.process_shipment.auth.service import login


async def buscar(datos_busqueda: BusquedaRequest) -> BusquedaResponse:
    """
    Ejecuta una búsqueda en Shalom con los datos del formulario.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = ShalomHttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()

        response = await client.client.post(
            "/envia_ya/person/search",
            headers=headers,
            json=datos_busqueda.model_dump(),
        )
        return response.json()
    finally:
        await client.close()
