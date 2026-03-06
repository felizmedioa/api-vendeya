from fastapi import APIRouter

from app.features.get_key.schemas import SetKeyRequest
from app.features.get_key.service import asignar_clave


router = APIRouter(
    tags=["Asignar/Actualizar clave"]
)

@router.post("/asignar-clave")
async def set_clave(
    datos: SetKeyRequest,
):
    return await asignar_clave(datos)