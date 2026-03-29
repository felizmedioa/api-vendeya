# ============================================================================
# routes.py — Endpoints para el código diario
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
        "la clave en memoria y envía notificación por Pushover. "
        "Ignora el guard de fecha (siempre rota)."
    ),
)
async def force_rotate_code():
    result = await rotate_daily_code(force=True)
    return result


@router.post(
    "/daily-code/simulate-midnight",
    summary="Simular rotación de medianoche",
    description=(
        "Ejecuta EXACTAMENTE el mismo flujo que se dispara a las 00:00. "
        "Respeta el guard de fecha: si ya se rotó hoy, retorna skipped. "
        "Útil para probar que la protección anti-duplicado funciona."
    ),
)
async def simulate_midnight():
    """
    Simula el disparo de medianoche.
    - Si ya se rotó hoy → retorna skipped (demuestra que el guard funciona)
    - Si no se ha rotado → genera código nuevo (mismo flujo que a las 00:00)
    """
    result = await rotate_daily_code(force=False)
    return result
