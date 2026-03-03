# ============================================================================
# main.py — Punto de entrada de la aplicación FastAPI
# ============================================================================
# Este es el archivo que uvicorn ejecuta:
#   uvicorn app.main:app --reload
#
# Responsabilidades de este archivo:
# 1. Crear la instancia de FastAPI
# 2. Configurar el lifespan (inicio/cierre del servidor)
# 3. Incluir los routers de cada feature
#
# NO debe contener lógica de negocio ni endpoints directamente.
# ============================================================================

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.features.auth.routes import router as auth_router
from app.features.envios.routes import router as envios_router
from app.features.filleo.routes import router as filleo_router
from app.features.productos.routes import router as productos_router
from app.features.search.routes import router as search_router
from app.features.usuarios.routes import router as usuarios_router
from app.features.delete_orders.routes import router as delete_orders_router
from app.features.preregister.routes import router as preregister_router
from app.features.register.routes import router as register_router
from app.features.get_key.routes import router as get_key_router
from app.features.terminals.routes import router as terminals_router
from app.features.process_shipment.routes import router as process_shipment_router
from app.shared.http_client import ShalomHttpClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan: se ejecuta al INICIAR y CERRAR el servidor.

    Crea UNA SOLA instancia de ShalomHttpClient durante toda la vida
    del servidor. Todos los features comparten el mismo cliente HTTP
    con las mismas cookies de sesión via app.state.
    """
    # STARTUP: Crear el cliente y guardarlo en app.state
    app.state.shalom_client = ShalomHttpClient()

    yield  # ← Aquí el servidor está activo y atendiendo peticiones

    # SHUTDOWN: Cerrar el cliente HTTP limpiamente
    await app.state.shalom_client.close()


app = FastAPI(
    title="API Shalom",
    description="API proxy para interactuar con pro.shalom.pe",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://pedido-repartos-lima-provincia.vercel.app",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite cualquier cabecera
)

# ============================================================================
# Registrar los routers de cada feature
# ============================================================================
app.include_router(auth_router)
app.include_router(envios_router)
app.include_router(filleo_router)
app.include_router(productos_router)
app.include_router(search_router)
app.include_router(usuarios_router)
app.include_router(delete_orders_router)
app.include_router(preregister_router)
app.include_router(register_router)
app.include_router(get_key_router)
app.include_router(terminals_router)
app.include_router(process_shipment_router)
