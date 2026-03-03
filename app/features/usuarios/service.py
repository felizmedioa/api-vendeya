# ============================================================================
# service.py — Lógica de usuarios con Shalom
# ============================================================================

from app.shared.http_client import ShalomHttpClient


async def get_user(shalom: ShalomHttpClient) -> dict:
    """
    Obtiene los datos del usuario autenticado.
    Requiere haber hecho login() previamente.
    """
    shalom.verificar_sesion()
    response = await shalom.client.get("/get-auth-user")
    return response.json()
