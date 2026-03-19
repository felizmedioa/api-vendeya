# ============================================================================
# main.py — Punto de entrada de la aplicación FastAPI
# ============================================================================
# Este es el archivo que uvicorn ejecuta:
#   uvicorn app.main:app --reload
#
# Responsabilidades de este archivo:
# 1. Crear la instancia de FastAPI
# 2. Incluir los routers de cada feature
#
# NO debe contener lógica de negocio ni endpoints directamente.
# Cada feature crea su propio HttpClient al recibir una llamada.
# ============================================================================

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.features.envios.routes import router as envios_router
from app.features.productos.routes import router as productos_router
from app.features.search.routes import router as search_router
from app.features.usuarios.routes import router as usuarios_router
from app.features.delete_orders.routes import router as delete_orders_router
from app.features.get_key.routes import router as get_key_router
from app.features.terminals.routes import router as terminals_router
from app.features.process_shipment.routes import router as process_shipment_router
from app.features.auth.routes import router as auth_router
from app.features.user.routes import router as user_router
from app.features.ping.routes import router as ping_router
from app.features.pedidos_forms.routes import router as pedidos_forms_router


app = FastAPI(
    title="API VendeYa",
    description="API proxy para interactuar con servicios externos",
    version="1.0.0",
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
app.include_router(envios_router)
app.include_router(productos_router)
app.include_router(search_router)
app.include_router(usuarios_router)
app.include_router(delete_orders_router)
app.include_router(get_key_router)
app.include_router(terminals_router)
app.include_router(process_shipment_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(ping_router)
app.include_router(pedidos_forms_router)
