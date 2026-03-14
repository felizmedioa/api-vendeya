# ============================================================================
# http_client.py — Cliente HTTP compartido para comunicarse con la API externa
# ============================================================================
# Este módulo contiene la clase base que encapsula el httpx.AsyncClient
# y los helpers comunes que usan todos los features (headers AJAX,
# verificación de sesión, etc.)
#
# Se instancia UNA VEZ en el lifespan de FastAPI y se comparte
# entre todos los features via app.state.
# ============================================================================

import urllib.parse

import httpx
from fastapi import HTTPException

from app.core.config import settings


class HttpClient:
    """
    Cliente HTTP base que mantiene la sesión con la API externa.

    Encapsula:
    - El httpx.AsyncClient con URL base y timeout
    - Verificación de sesión activa
    - Generación de headers AJAX con XSRF-TOKEN
    """

    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url=settings.CLIENT_BASE_URL,
            timeout=settings.CLIENT_TIMEOUT,
        )

    async def close(self):
        """Cierra el cliente HTTP. Se llama al apagar el servidor."""
        await self.client.aclose()

    def verificar_sesion(self):
        """
        Verifica que exista una sesión activa (cookie enviashalom_session).
        Lanza HTTP 401 si no hay sesión.
        """
        if not self.client.cookies.get("enviashalom_session"):
            raise HTTPException(
                status_code=401,
                detail="No hay sesión activa. Llama primero a /obtener-token",
            )

    def obtener_headers_ajax(self) -> dict:
        """
        Genera los headers necesarios para peticiones AJAX.

        - X-Requested-With: Laravel verifica que sea AJAX
        - x-xsrf-token: Protección CSRF (decodificado de la cookie)
        - Referer: Algunos servidores verifican el origen
        """
        xsrf_token = urllib.parse.unquote(
            self.client.cookies.get("XSRF-TOKEN", "")
        )
        return {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": f"{settings.CLIENT_BASE_URL}/",
            "x-xsrf-token": xsrf_token,
        }
