# ============================================================================
# service.py — Lógica de login de usuario
# ============================================================================

import logging

import httpx
from fastapi import HTTPException

from app.features.auth.login.schemas import LoginRequest, LoginResponse
from app.features.auth.service import (
    crear_token_JWT,
    decodificar_token_JWT,
    verificar_password,
)
from app.core.config import settings

logger = logging.getLogger("auth.login")


async def login_user(datos: LoginRequest) -> LoginResponse:
    """
    Inicia sesión de un usuario.

    Flujo:
    1. Si viene token JWT → validar y renovar
    2. Si vienen credenciales → buscar en Google Script → verificar password → generar JWT
    """

    # ── Caso A: Login con token JWT existente ────────────────────────
    if datos.token:
        payload = decodificar_token_JWT(datos.token)

        if payload:
            # Token válido → renovar y retornar
            token_renovado = crear_token_JWT(
                payload.get("username", ""),
                payload.get("sub", ""),
            )
            return LoginResponse(
                success=True,
                message="Sesión válida",
                token=token_renovado,
            )
        else:
            # Token inválido o expirado
            return LoginResponse(
                success=False,
                message="Debe iniciar sesión nuevamente",
            )

    # ── Caso B: Login con credenciales ───────────────────────────────
    if not datos.user or not datos.password:
        return LoginResponse(
            success=False,
            message="Debe enviar usuario y contraseña, o un token válido",
        )

    # ── Buscar usuario en Google Script ──────────────────────────────
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(
                settings.GOOGLE_SCRIPT_URL,
                params={"action": "login", "user": datos.user},
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al buscar usuario: {exc}")
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

    # ── Verificar si el usuario existe ───────────────────────────────
    status = data.get("status", "").lower()

    if status == "error":
        return LoginResponse(
            success=False,
            message="El usuario no existe",
        )

    # ── Verificar contraseña ─────────────────────────────────────────
    hash_almacenado = data.get("password", "")
    user_id = data.get("userId", "")

    if not verificar_password(datos.password, hash_almacenado):
        return LoginResponse(
            success=False,
            message="Contraseña incorrecta",
        )

    # ── Login exitoso → generar JWT ──────────────────────────────────
    token = crear_token_JWT(datos.user, user_id)

    return LoginResponse(
        success=True,
        message="Inicio de sesión exitoso",
        token=token,
    )
