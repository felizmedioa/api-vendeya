from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.shared.http_client import ShalomHttpClient
from app.features.register.service import registrar_orden
from app.features.register.schemas import RegisterRequest

router = APIRouter(
    tags=["Registro"],
)

@router.post(
    "/registrar",
    summary="Registrar",
    description="Endpoint para registrar",
)
async def registrar(
    claves: RegisterRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await registrar_orden(client, claves)
