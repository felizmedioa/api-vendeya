# ============================================================================
# service.py — Orquestador del feature auth
# ============================================================================
# Lógica compartida entre login y register:
# - Generación de JWT
# - Verificación de JWT
# - Verificación de contraseñas
# ============================================================================

from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Contexto de hashing con argon2 (compartido con register)
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def crear_token_JWT(user: str, user_id: str) -> str:
    """Genera un JWT con los datos del usuario. Expira en 24 horas."""
    payload = {
        "sub": user_id,
        "username": user,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24),
    }
    return jwt.encode(payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def decodificar_token_JWT(token: str) -> dict | None:
    """
    Decodifica y valida un JWT.
    Retorna el payload si es válido, None si es inválido o expiró.
    """
    try:
        payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verificar_password(password_plano: str, hash_almacenado: str) -> bool:
    """Compara una contraseña en texto plano contra un hash argon2."""
    return pwd_context.verify(password_plano, hash_almacenado)