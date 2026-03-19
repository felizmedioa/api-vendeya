# ============================================================================
# service.py — Lógica para señalización de pedidos impresos
# ============================================================================

import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings

logger = logging.getLogger("pedidos_forms.signal")


async def update_pedidos_status(pedidos_ids: list[str], nuevo_estado: str = "Impreso"):
    """
    Actualiza el estado de una lista de pedidos en Google Sheets.

    Flujo:
    1. Preparar el payload con la acción 'update_status'
    2. Ejecutar tarea secundaria independiente
    3. Enviar petición a Google Apps Script
    4. Interpretar y retornar respuesta
    """

    # ── Paso 1: Preparar payload ─────────────────────────────────────
    payload = {
        "action": "update_status",
        "pedidos_ids": pedidos_ids,
        "nuevo_estado": nuevo_estado
    }
    
    # ── Paso 2: Ejecutar Tarea Secundaria Independiente ──────────────
    # Aquí puedes insertar la lógica que el sistema deba hacer en backend
    # independientemente.
    # Por ejemplo: Generar un PDF en S3, descontar saldo, notificar, etc.
    # ejemplo_tarea_secundaria(pedidos_ids)

    # ── Paso 3: Consultar Google Apps Script ─────────────────────────
    # Asegúrate de tener APPS_SCRIPT_PEDIDOS_FORMS_URL en tu app/core/config.py
    
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                settings.APPS_SCRIPT_PEDIDOS_FORMS_URL,
                json=payload,
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al actualizar estado de pedidos: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    if response.status_code != 200:
        logger.error(
            f"Google Script respondió con status {response.status_code}"
        )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    try:
        data = response.json()
    except Exception:
        logger.error("Respuesta de Google Script no es JSON válido")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    # ── Paso 4: Interpretar la respuesta ─────────────────────────────
    status = data.get("status", "").lower()

    if status == "error":
        raise HTTPException(
            status_code=400,
            detail=data.get("message", "Error al actualizar los pedidos"),
        )

    return data
