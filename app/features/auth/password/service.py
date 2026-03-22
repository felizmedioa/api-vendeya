import logging

import httpx
from fastapi import HTTPException
from passlib.context import CryptContext

from app.core.config import settings
from app.features.auth.password.schemas import ChangePasswordRequest, ChangePasswordResponse
from app.features.auth.service import decodificar_token_JWT, verificar_password

logger = logging.getLogger("auth.password")

# Contexto de hashing con argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea la nueva contraseña usando argon2."""
    return pwd_context.hash(password)


async def change_password(datos: ChangePasswordRequest) -> ChangePasswordResponse:
    """
    Cambia la contraseña de un usuario validando primero su JWT
    y su contraseña actual.
    """
    # ── 1. Validar el token JWT ──────────────────────────────────────
    payload = decodificar_token_JWT(datos.token)
    if not payload:
        return ChangePasswordResponse(
            success=False,
            message="Token inválido o expirado",
        )

    user_id = payload.get("sub", "")
    username = payload.get("username", "")

    # ── 2. Obtener el usuario actual desde Google Script ─────────────
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                settings.GOOGLE_SCRIPT_URL,
                params={"action": "login", "user": username},
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al buscar usuario para cambio de pass: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    if response.status_code != 200:
        logger.error(f"Google Script respondió con status {response.status_code}")
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

    if data.get("status", "").lower() == "error":
        return ChangePasswordResponse(
            success=False,
            message="El usuario no existe",
        )

    # ── 3. Verificar contraseña antigua ──────────────────────────────
    hash_almacenado = data.get("password", "")

    if not verificar_password(datos.old_password, hash_almacenado):
        return ChangePasswordResponse(
            success=False,
            message="Contraseña actual incorrecta",
        )

    # ── 4. Hashear y actualizar en Google Script ─────────────────────
    nuevo_hash = hash_password(datos.new_password)

    payload_update = {
        "action": "update_password",
        "userId": user_id,
        "newPassword": nuevo_hash,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            update_response = await client.post(
                settings.GOOGLE_SCRIPT_URL,
                json=payload_update,
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al actualizar contraseña: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno al actualizar la contraseña.",
        )

    if update_response.status_code != 200:
        logger.error("Fallo al actualizar contraseña en Google Script.")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    update_data = update_response.json()
    if update_data.get("status", "").lower() == "error":
        return ChangePasswordResponse(
            success=False,
            message="Error al intentar actualizar la nueva contraseña en DB",
        )

    return ChangePasswordResponse(
        success=True,
        message="Contraseña actualizada exitosamente",
    )
