# ============================================================================
# service.py — Lógica de negocio del feature user
# ============================================================================

from app.features.user.schemas import UserResponse, UserUpdateRequest


async def get_current_user() -> UserResponse:
    """
    Obtiene los datos del usuario autenticado.

    TODO: Implementar lógica para obtener el usuario desde el token JWT
    o la sesión activa.
    """
    raise NotImplementedError("Obtener usuario aún no implementado")


async def update_user(datos: UserUpdateRequest) -> UserResponse:
    """
    Actualiza los datos de un usuario.

    TODO: Implementar lógica de actualización en base de datos.
    """
    raise NotImplementedError("Actualizar usuario aún no implementado")
