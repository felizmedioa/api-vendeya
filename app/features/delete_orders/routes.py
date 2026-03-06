from fastapi import APIRouter

from app.features.delete_orders.service import eliminar_ordenes

router = APIRouter(
    tags=["Eliminar ordenes"],
)

@router.post(
    "/eliminar-ordenes",
    summary="Eliminar ordenes",
    description="Elimina una o varias ordenes",
)
async def delete_orders(
    id: int,
):
    return await eliminar_ordenes(id)
