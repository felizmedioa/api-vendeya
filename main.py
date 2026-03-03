from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, HTTPException
import httpx, urllib.parse
from bs4 import BeautifulSoup



@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http_client = httpx.AsyncClient(
        base_url="https://pro.shalom.pe",
        timeout=10
    )
    yield
    await app.state.http_client.aclose()

app = FastAPI(lifespan=lifespan)

@app.get("/obtener-token")
async def get_token_login(request: Request):
    
    client = request.app.state.http_client
    response = await client.get("/login?origin=WEB")
    html_unfind = response.text 

    soup = BeautifulSoup(html_unfind, 'html.parser')
    token = soup.find("input", {"name": "_token"})["value"]
    
    datos_login = {
        "_token": token,
        "email": "cv.cr.importadores@gmail.com",
        "password": "coin73@U",   
    }

    response_login = await client.post("/login", data=datos_login, follow_redirects=True)

    if "dashboard" in str(response_login.url) or response_login.status_code == 200:
        cookie_token_crudo = client.cookies.get("XSRF-TOKEN", "")
        token_limpio = urllib.parse.unquote(cookie_token_crudo)
        return {
            "estado": "exito",
            "mensaje": "Sesión iniciada correctamente. El backend ya tiene las cookies listas.",
            "xsrf_token": token_limpio
        }
    else:
        raise HTTPException(
            status_code=401, 
            detail="Credenciales incorrectas o el login falló"
        )

@app.get("/obtener-datos")
async def get_datos(request: Request):
    client = request.app.state.http_client
    response = await client.get("/get-auth-user")
    return response.json()

@app.post("/obtener-productos")
async def get_productos(request: Request):
    client = request.app.state.http_client

    # Verificar que haya sesión activa
    if not client.cookies.get("enviashalom_session"):
        raise HTTPException(
            status_code=401,
            detail="No hay sesión activa. Llama primero a /obtener-token"
        )

    # Leer el XSRF-TOKEN directamente de las cookies del cliente
    xsrf_token = urllib.parse.unquote(client.cookies.get("XSRF-TOKEN", ""))

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://pro.shalom.pe/",
        "x-xsrf-token": xsrf_token,
    }

    response = await client.post("/envia_ya/products", headers=headers)
    return response.json()

@app.post("/crear-envio")
async def crear_envio(request: Request):
    client = request.app.state.http_client

    # Verificar que haya sesión activa
    if not client.cookies.get("enviashalom_session"):
        raise HTTPException(
            status_code=401,
            detail="No hay sesión activa. Llama primero a /obtener-token"
        )

    # Leer el XSRF-TOKEN directamente de las cookies del cliente
    xsrf_token = urllib.parse.unquote(client.cookies.get("XSRF-TOKEN", ""))

    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://pro.shalom.pe/",
        "x-xsrf-token": xsrf_token,
    }

    datos_envio = {"origen":9,"destino":7,"tipo_pago":"REMITENTE","tipo_producto":3,"tipo_producto_json":{"value":8,"name":"Sobre","detalle":"Documentos simples en sobre manila / Tamaño A4"},"cantidad":1,"peso":"","alto":"","largo":"","ancho":"","costo":8,"remitente":"73530477","destinatario":"70951063","remitente_id":555087,"destinatario_id":4071047,"garantia":0,"garantia_costo":0,"garantia_monto":"0.00","contacto_doc":"","grrs":"[]","clave":"1254","aereo":0,"servicio_cobranza":0,"servicio_cobranza_costo":0,"servicio_cobranza_datos":"{\"document\":\"\",\"name\":\"\",\"bank\":\"\",\"type_account\":\"\",\"account_number\":\"\",\"cci\":\"\"}","declaracion_jurada":""}

    response = await client.post("/envia_ya/service_order/save", headers=headers, json=datos_envio)
    return response.json()