# ============================================================================
# service.py — Lógica para actualizar configuraciones del usuario
# ============================================================================

import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.features.auth.service import decodificar_token_JWT
from app.features.user.update.schemas import (
    UserUpdateConfigRequest,
    UserUpdateConfigResponse,
)

logger = logging.getLogger("user.update")


async def update_user_config(
    token: str, datos: UserUpdateConfigRequest
) -> UserUpdateConfigResponse:
    """
    Actualiza las configuraciones del usuario en Google Sheet.

    Flujo:
    1. Validar el JWT y extraer user_id
    2. Enviar los datos validados + user_id a Google Apps Script (vía POST)
    3. Retornar la respuesta de éxito o fallo
    """

    # ── Paso 1: Validar JWT ──────────────────────────────────────────
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

    # ── Paso 2: Preparar payload para Google Script ──────────────────
    # Añadimos action="update_config" y el user_id a los datos puros
    payload_gs = {
        "action": "update_config",
        "user_id": str(user_id),
        **datos.model_dump(),
    }

    # ── Paso 3: Enviar POST a Google Apps Script ─────────────────────
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                settings.GOOGLE_SCRIPT_CONFIG_URL,
                json=payload_gs,
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al actualizar configuraciones: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    if response.status_code != 200:
        logger.error(
            f"Google Script Config respondió status {response.status_code}"
        )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    try:
        data = response.json()
    except Exception:
        logger.error("Respuesta de Google Script (POST) no es JSON válido")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    # ── Paso 4: Interpretar respuesta ────────────────────────────────
    status = data.get("status", "").lower()

    if status == "error":
        logger.error(f"Error desde Google Script: {data.get('message')}")
        raise HTTPException(
            status_code=500,
            detail=data.get("message", "Error al guardar configuraciones"),
        )

    return UserUpdateConfigResponse(
        success=True,
        message="Configuraciones guardadas correctamente.",
    )
