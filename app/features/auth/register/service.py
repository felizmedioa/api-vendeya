# ============================================================================
# service.py — Lógica de registro de usuario
# ============================================================================

import logging

import httpx
from fastapi import HTTPException
from passlib.context import CryptContext

from app.features.auth.register.schemas import RegisterRequest, RegisterResponse
from app.core.config import settings

from app.features.auth.service import crear_token_JWT

logger = logging.getLogger("auth.register")

# Contexto de hashing con argon2
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea una contraseña usando argon2."""
    return pwd_context.hash(password)


async def register_user(datos: RegisterRequest) -> RegisterResponse:
    """
    Registra un nuevo usuario enviando los datos a Google Apps Script.

    Flujo:
    1. Hashear la contraseña con argon2
    2. Enviar user + contraseña hasheada al endpoint de Google Script
    3. Interpretar respuesta y manejar errores
    """
    # ── Paso 1: Hashear la contraseña ────────────────────────────────
    hashed_password = hash_password(datos.password)

    # ── Paso 2: Enviar datos al Google Script ────────────────────────
    payload = {
        "user": datos.user,
        "password": hashed_password,
    }

    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                settings.GOOGLE_SCRIPT_URL,
                json=payload,
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al registrar usuario: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    # ── Paso 3: Interpretar la respuesta ─────────────────────────────
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

    # ── Manejar errores del Google Script ────────────────────────────
    status = data.get("status", "").lower()
    message = data.get("message", "")

    if status == "error":
        error_type = message.lower()

        # Único error específico que se expone al frontend
        if "ya existe" in error_type or "already exists" in error_type or "duplicate" in error_type:
            raise HTTPException(
                status_code=409,
                detail="El usuario ya existe.",
            )

        # Cualquier otro error → genérico
        logger.error(f"Error del Google Script: {message}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    # ── Registro exitoso ─────────────────────────────────────────────
    return RegisterResponse(
        success=True,
        message=data.get("message", "Usuario registrado correctamente"),
        token=crear_token_JWT(datos.user, data.get("userId")),
    )
