# ============================================================================
# routes.py — Endpoints de autenticación
# ============================================================================

from fastapi import APIRouter

from app.features.auth.login.schemas import LoginRequest, LoginResponse
from app.features.auth.login.service import login_user
from app.features.auth.register.schemas import RegisterRequest, RegisterResponse
from app.features.auth.register.service import register_user

router = APIRouter(
    prefix="/auth",
    tags=["Auth"],
)


@router.post(
    "/login",
    response_model=LoginResponse,
    summary="Iniciar sesión",
    description="Autentica un usuario con email y contraseña.",
)
async def login_endpoint(datos: LoginRequest):
    return await login_user(datos)


@router.post(
    "/register",
    response_model=RegisterResponse,
    summary="Registrar usuario",
    description="Registra un nuevo usuario en la aplicación.",
)
async def register_endpoint(datos: RegisterRequest):
    return await register_user(datos)
