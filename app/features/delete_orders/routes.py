from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.shared.http_client import ShalomHttpClient
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
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await eliminar_ordenes(client, id)
