# ============================================================================
# routes.py — Endpoint de envíos
# ============================================================================

from fastapi import APIRouter

from app.features.envios.schemas import DatosEnvio
from app.features.envios.service import crear_envio

router = APIRouter(
    tags=["Envíos"],
)


@router.post(
    "/crear-envio",
    summary="Crear una orden de envío",
    description="Crea un envío en Shalom con los datos proporcionados.",
)
async def crear_envio_endpoint(
    datos: DatosEnvio,
):
    return await crear_envio(datos.model_dump())
