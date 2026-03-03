# ============================================================================
# routes.py — Endpoint de productos
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.productos.service import get_productos
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Productos"],
)


@router.post(
    "/obtener-productos",
    summary="Listar productos de Envía Ya",
    description="Obtiene todos los productos disponibles. Requiere sesión activa.",
)
async def obtener_productos(
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await get_productos(client)
