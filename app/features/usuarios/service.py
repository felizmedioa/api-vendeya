# ============================================================================
# service.py — Lógica de usuarios con Shalom
# ============================================================================

from app.shared.http_client import ShalomHttpClient
from app.features.process_shipment.auth.service import login


async def get_user() -> dict:
    """
    Obtiene los datos del usuario autenticado.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = ShalomHttpClient()
    try:
        await login(client)
        response = await client.client.get("/get-auth-user")
        return response.json()
    finally:
        await client.close()
