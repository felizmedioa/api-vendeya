# ============================================================================
# daily_code_service.py — Orquestación del código diario
# ============================================================================
# Funciones:
#   rotate_daily_code()    → genera código → Google Sheets → Pushover → settings
#   sync_code_from_sheets() → lee el código actual de Google Sheets al arrancar
#   log_code_to_sheets()    → registra un código en Google Sheets
# ============================================================================

import asyncio
import logging
from datetime import datetime

import httpx

from app.core.config import settings
from app.features.process_shipment.set_code.service import (
    generate_code,
    send_pushover_notification,
)

logger = logging.getLogger("daily_code")

# ── Protección anti-duplicado ────────────────────────────────────────────────
# _rotate_lock: evita ejecuciones concurrentes dentro del mismo proceso
# _last_rotation_date: guarda la fecha de la última rotación exitosa
_rotate_lock = asyncio.Lock()
_last_rotation_date: str | None = None


async def log_code_to_sheets(code: str, fecha: str) -> dict | None:
    """
    Registra el código y la fecha en Google Sheets vía Apps Script.
    Retorna None si GOOGLE_SCRIPT_CODIGOS no está configurado.
    """
    url = settings.GOOGLE_SCRIPT_CODIGOS
    if not url:
        logger.warning("GOOGLE_SCRIPT_CODIGOS no configurado, omitiendo registro en Sheets.")
        return None

    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            url,
            json={"codigo": code, "fecha": fecha},
            follow_redirects=True,
        )
        result = response.json()
        logger.info(f"Google Sheets → {result}")
        return result


async def sync_code_from_sheets() -> str | None:
    """
    Lee el último código registrado en Google Sheets.
    Se usa al arrancar la app para sincronizar CLAVE_PAQUETE.
    También sincroniza _last_rotation_date si el código es de hoy,
    para evitar rotaciones duplicadas tras un reinicio.
    Retorna None si no hay conexión o no hay códigos.
    """
    global _last_rotation_date

    url = settings.GOOGLE_SCRIPT_CODIGOS
    if not url:
        logger.info("GOOGLE_SCRIPT_CODIGOS no configurado, usando CLAVE_PAQUETE del .env")
        return None

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(url, follow_redirects=True)
            data = response.json()

            if data.get("success") and data.get("codigo"):
                code = data["codigo"]
                settings.CLAVE_PAQUETE = code
                logger.info(f"Código sincronizado desde Sheets: {code}")

                # Si el código en Sheets ya es de hoy, marcar como rotado
                fecha_sheets = data.get("fecha", "")
                fecha_hoy = datetime.now().strftime("%Y-%m-%d")
                if fecha_sheets == fecha_hoy:
                    _last_rotation_date = fecha_hoy
                    logger.info(f"Código de hoy ya existe en Sheets, marcando como rotado ({fecha_hoy})")

                return code
            else:
                logger.info("No hay códigos en Sheets aún.")
                return None
    except Exception as exc:
        logger.error(f"Error sincronizando desde Sheets: {exc}")
        return None


async def rotate_daily_code(force: bool = False) -> dict:
    """
    Flujo completo de rotación diaria:
      1. Lee el código anterior de settings
      2. Genera uno nuevo (cumpliendo las 3 reglas)
      3. Lo registra en Google Sheets
      4. Actualiza settings.CLAVE_PAQUETE en memoria
      5. Envía notificación por Pushover

    Parámetros:
      force: si es True, omite el guard de fecha y rota siempre.
             Útil para simulación y forzar rotación manual.

    Retorna un dict con el resultado de la operación.
    """
    global _last_rotation_date

    async with _rotate_lock:
        fecha = datetime.now().strftime("%Y-%m-%d")

        # ── Guard: no rotar más de 1 vez por día (salvo force=True) ──
        if not force and _last_rotation_date == fecha:
            logger.info(f"Código ya fue rotado hoy ({fecha}), omitiendo ejecución duplicada.")
            return {
                "success": True,
                "skipped": True,
                "reason": f"Ya se rotó hoy ({fecha})",
                "current_code": settings.CLAVE_PAQUETE,
                "fecha": fecha,
            }

        previous_code = settings.CLAVE_PAQUETE
        new_code = generate_code(previous_code)

        logger.info(f"Rotando código: {previous_code} → {new_code} (fecha: {fecha}, force: {force})")

        # 1. Registrar en Google Sheets
        sheets_result = await log_code_to_sheets(new_code, fecha)

        # 2. Actualizar en memoria
        settings.CLAVE_PAQUETE = new_code
        _last_rotation_date = fecha  # Marcar como rotado
        logger.info(f"CLAVE_PAQUETE actualizado en memoria: {new_code}")

        # 3. Notificar por Pushover
        try:
            pushover_result = await send_pushover_notification(new_code)
            logger.info(f"Pushover → {pushover_result}")
        except Exception as exc:
            logger.error(f"Error enviando Pushover: {exc}")
            pushover_result = {"error": str(exc)}

        return {
            "success": True,
            "skipped": False,
            "forced": force,
            "previous_code": previous_code,
            "new_code": new_code,
            "fecha": fecha,
            "sheets": sheets_result,
            "pushover": pushover_result,
        }
