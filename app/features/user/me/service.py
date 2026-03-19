# ============================================================================
# service.py — Lógica para obtener configuraciones del usuario
# ============================================================================

import logging

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.features.auth.service import decodificar_token_JWT
from app.features.user.me.schemas import UserConfig, UserConfigResponse

logger = logging.getLogger("user.me")


async def get_user_config(token: str) -> UserConfigResponse:
    """
    Obtiene las configuraciones del usuario desde Google Sheet.

    Flujo:
    1. Validar el JWT y extraer user_id
    2. Consultar Google Apps Script con el user_id
    3. Retornar las configuraciones o mensaje de que no existen
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

    # ── Paso 2: Consultar Google Apps Script ─────────────────────────
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                settings.GOOGLE_SCRIPT_CONFIG_URL,
                params={"user_id": user_id},
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al obtener configuraciones: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    if response.status_code != 200:
        logger.error(
            f"Google Script Config respondió con status {response.status_code}"
        )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    try:
        data = response.json()
    except Exception:
        logger.error("Respuesta de Google Script Config no es JSON válido")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    # ── Paso 3: Interpretar la respuesta ─────────────────────────────
    status = data.get("status", "").lower()

    # Error del Google Script (usuario no encontrado, etc.)
    if status == "error":
        return UserConfigResponse(
            success=True,
            message=data.get("message", "No tiene configuraciones definidas"),
        )

    # Verificar si las configuraciones ya están creadas
    create_config = _to_bool(data.get("create_config", 0))

    if not create_config:
        return UserConfigResponse(
            success=True,
            message="No tiene configuraciones definidas",
        )

    # ── Configuraciones encontradas ──────────────────────────────────
    config = UserConfig(
        id=str(data.get("id", user_id)),
        shalom=_to_bool(data.get("shalom", 0)),
        marvisur=_to_bool(data.get("marvisur", 0)),
        delivery=_to_bool(data.get("delivery", 0)),
        dinsides=_to_bool(data.get("dinsides", 0)),
        olva=_to_bool(data.get("olva", 0)),
        retiro_tienda=_to_bool(data.get("retiro_tienda", 0)),
        create_config=True,
        telefono=str(data.get("telefono", "")),
        nombre_empresa=str(data.get("nombre_empresa", "")),
    )

    return UserConfigResponse(
        success=True,
        message="Configuraciones obtenidas correctamente",
        config=config,
    )


def _to_bool(value) -> bool:
    """Convierte valores 1/0, '1'/'0', True/False a bool."""
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value == 1
    if isinstance(value, str):
        return value.strip() in ("1", "true", "True")
    return False
