# ============================================================================
# routes.py — Endpoint de productos
# ============================================================================

from fastapi import APIRouter

from app.features.productos.service import get_productos

router = APIRouter(
    tags=["Productos"],
)


@router.post(
    "/obtener-productos",
    summary="Listar productos de Envía Ya",
    description="Obtiene todos los productos disponibles.",
)
async def obtener_productos():
    return await get_productos()
