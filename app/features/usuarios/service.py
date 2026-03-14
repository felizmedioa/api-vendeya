# ============================================================================
# service.py — Lógica de usuarios
# ============================================================================

from app.shared.http_client import HttpClient
from app.features.process_shipment.auth.service import login


async def get_user() -> dict:
    """
    Obtiene los datos del usuario autenticado.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = HttpClient()
    try:
        await login(client)
        response = await client.client.get("/get-auth-user")
        return response.json()
    finally:
        await client.close()
