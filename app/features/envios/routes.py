# ============================================================================
# routes.py — Endpoint de envíos
# ============================================================================

from fastapi import APIRouter, Depends

from app.core.dependencies import get_shalom_client
from app.features.envios.schemas import DatosEnvio
from app.features.envios.service import crear_envio
from app.shared.http_client import ShalomHttpClient

router = APIRouter(
    tags=["Envíos"],
)


@router.post(
    "/crear-envio",
    summary="Crear una orden de envío",
    description="Crea un envío en Shalom con los datos proporcionados. Requiere sesión activa.",
)
async def crear_envio_endpoint(
    datos: DatosEnvio,
    client: ShalomHttpClient = Depends(get_shalom_client),
):
    return await crear_envio(client, datos.model_dump())
