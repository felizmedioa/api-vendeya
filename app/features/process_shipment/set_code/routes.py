# ============================================================================
# routes.py — Endpoint para forzar rotación manual del código diario
# ============================================================================

from fastapi import APIRouter

from app.features.process_shipment.set_code.daily_code_service import (
    rotate_daily_code,
)

router = APIRouter(
    tags=["Código Diario"],
)


@router.post(
    "/daily-code/force-rotate",
    summary="Forzar rotación del código diario",
    description=(
        "Ejecuta manualmente la rotación del código de seguridad: "
        "genera uno nuevo, lo registra en Google Sheets, actualiza "
        "la clave en memoria y envía notificación por Pushover."
    ),
)
async def force_rotate_code():
    result = await rotate_daily_code()
    return result
