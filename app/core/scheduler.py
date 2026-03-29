# ============================================================================
# scheduler.py — Scheduler para rotación automática de código diario
# ============================================================================
# Usa APScheduler con CronTrigger para ejecutar a las 00:00 hora Lima.
# ============================================================================

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

logger = logging.getLogger("scheduler")

scheduler = AsyncIOScheduler()


async def _run_rotate():
    """Wrapper para ejecutar rotate_daily_code dentro del scheduler."""
    # Import diferido para evitar imports circulares
    from app.features.process_shipment.set_code.daily_code_service import (
        rotate_daily_code,
    )

    try:
        result = await rotate_daily_code()
        logger.info(f"Rotación diaria completada: {result}")
    except Exception as exc:
        logger.error(f"Error en rotación diaria: {exc}", exc_info=True)


def start_scheduler():
    """
    Inicia el scheduler con un CronTrigger:
    - Ejecuta a las 00:00 hora Lima (America/Lima, UTC-5)
    - Todos los días
    """
    scheduler.add_job(
        _run_rotate,
        CronTrigger(hour=0, minute=0, timezone="America/Lima"),
        id="daily_code_rotation",
        name="Rotación diaria de código",
        replace_existing=True,
        coalesce=True,              # Fusionar múltiples fires pendientes en 1
        misfire_grace_time=60,      # Solo ejecutar si el retraso es < 60s
        max_instances=1,            # No permitir ejecuciones paralelas
    )
    scheduler.start()
    logger.info("Scheduler iniciado — próxima ejecución: 00:00 America/Lima")


def shutdown_scheduler():
    """Detiene el scheduler limpiamente."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler detenido.")
