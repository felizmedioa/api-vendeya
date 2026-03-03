# ============================================================================
# service.py — Lógica de envíos con Shalom
# ============================================================================

from app.shared.http_client import ShalomHttpClient


async def crear_envio(shalom: ShalomHttpClient, datos_envio: dict) -> dict:
    """
    Crea una orden de servicio (envío) en Shalom.

    Args:
        shalom: Cliente HTTP con sesión activa.
        datos_envio: Diccionario con los datos del envío validados por el schema.
    """
    shalom.verificar_sesion()
    headers = shalom.obtener_headers_ajax()
    response = await shalom.client.post(
        "/envia_ya/service_order/save",
        headers=headers,
        json=datos_envio,
    )
    return response.json()
