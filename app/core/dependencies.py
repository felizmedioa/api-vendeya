# ============================================================================
# dependencies.py — Inyección de dependencias compartidas
# ============================================================================
# Centraliza la obtención del cliente HTTP compartido.
# Se usa en los endpoints con Depends(get_shalom_client).
# ============================================================================

from fastapi import Request

from app.shared.http_client import ShalomHttpClient


def get_shalom_client(request: Request) -> ShalomHttpClient:
    """
    Extrae el ShalomHttpClient de app.state.

    Se usa en los endpoints así:
        @router.get("/ruta")
        async def mi_endpoint(client: ShalomHttpClient = Depends(get_shalom_client)):
            ...
    """
    return request.app.state.shalom_client
