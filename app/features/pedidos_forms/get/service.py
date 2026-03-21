# ============================================================================
# service.py — Lógica para obtener listado de pedidos de formularios
# ============================================================================

import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.features.auth.service import decodificar_token_JWT

logger = logging.getLogger("pedidos_forms.get")


async def get_pedidos_by_client(token: str) -> list:
    """
    Obtiene los pedidos asociados a un cliente desde Google Sheets.

    Flujo:
    1. Validar Token JWT
    2. Consultar a Google Apps Script por id_usuario
    3. Retornar el arreglo de datos o una lista vacía
    """
    payload = decodificar_token_JWT(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Sesión expirada. Inicie sesión nuevamente.",
        )

    user_id = payload.get("sub", "")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Token inválido. No contiene ID de usuario.",
        )

    # ── Paso 1: Consultar Google Apps Script ─────────────────────────
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                settings.APPS_SCRIPT_PEDIDOS_FORMS_URL,
                params={"id_usuario": user_id},
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al obtener pedidos: {exc}")
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

    # ── Paso 3: Interpretar la respuesta ─────────────────────────────
    status = data.get("status", "").lower()

    if status == "error":
        raise HTTPException(
            status_code=400,
            detail=data.get("message", "Error al consultar los pedidos"),
        )

    return data.get("data", [])
