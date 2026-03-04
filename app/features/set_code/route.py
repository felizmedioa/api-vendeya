from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.set_code.schemas import SetCodeRequest, SetCodeResponse
from app.features.set_code.service import set_code
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Set Code"],
)


@router.post(
    "/set-code",
    description = "Asignar Código a los Envios",
    summary = "Asignar Código a los Envios",
)
async def asignar_codigo(
    datos: SetCodeRequest,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await set_code(client, datos)