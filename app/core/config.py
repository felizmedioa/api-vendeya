# ============================================================================
# config.py — Configuración global del proyecto
# ============================================================================
# ¿Por qué aquí?
# Centralizar TODA la configuración en un solo lugar permite:
#   1. Cambiar valores sin tocar el código (solo editas .env)
#   2. No exponer credenciales en el código fuente
#   3. Tener valores por defecto seguros
#
# Usamos pydantic-settings que lee automáticamente el archivo .env
# ============================================================================

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configuración de la aplicación.
    Los valores se leen del archivo .env automáticamente.
    Si no existen en .env, se usan los valores por defecto definidos aquí.
    """

    # URL base del sitio externo
    CLIENT_BASE_URL: str = "https://pro.shalom.pe"

    # Credenciales para iniciar sesión
    CLIENT_EMAIL: str = ""
    CLIENT_PASSWORD: str = ""

    # Timeout para las peticiones HTTP (en segundos)
    CLIENT_TIMEOUT: int = 30

    # Agencia de origen
    AGENCIA_ORIGEN: str = "HUAYCAN AV HORACIO ZEVALLOS"
    
    # Tipo de paquete
    TIPO_PAQUETE: str = "PAQUETE XXS"

    # Clave de paquete
    CLAVE_PAQUETE: str = "0246"

    # URL del Google Apps Script para registro de usuarios
    GOOGLE_SCRIPT_URL: str = ""

    # JWT
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"

    class Config:
        # Le dice a pydantic-settings que busque el archivo .env
        # en la raíz del proyecto
        env_file = ".env"


# Instancia única de la configuración.
# Se importa en otros módulos como: from app.core.config import settings
settings = Settings()
