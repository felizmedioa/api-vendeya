# ============================================================================
# service.py — Lógica de búsqueda con Shalom
# ============================================================================

from app.features.search.schemas import BusquedaRequest, BusquedaResponse
from app.shared.http_client import ShalomHttpClient


async def buscar(shalom: ShalomHttpClient, datos_busqueda: BusquedaRequest) -> BusquedaResponse:
    """
    Ejecuta una búsqueda en Shalom con los datos del formulario.

    Args:
        shalom: Cliente HTTP con sesión activa.
        datos_busqueda: Diccionario con los filtros de búsqueda validados.

    Returns:
        Respuesta JSON de Shalom.
    """
    shalom.verificar_sesion()
    headers = shalom.obtener_headers_ajax()

    response = await shalom.client.post(
        "/envia_ya/person/search",
        headers=headers,
        json=datos_busqueda.model_dump(),
    )
    return response.json()
