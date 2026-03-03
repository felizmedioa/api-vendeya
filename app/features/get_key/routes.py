from fastapi import APIRouter, Depends
from app.core.dependencies import get_shalom_client
from app.shared.http_client import ShalomHttpClient
from app.features.get_key.schemas import SetKeyRequest
from app.features.get_key.service import asignar_clave


router = APIRouter(
    tags=["Asignar/Actualizar clave"]
)

@router.post("/asignar-clave")
async def set_clave(
    datos: SetKeyRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await asignar_clave(client, datos)