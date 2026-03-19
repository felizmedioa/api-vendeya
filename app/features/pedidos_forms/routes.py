from fastapi import APIRouter
from app.features.pedidos_forms.create.schemas import PedidoFormCreate, PedidoFormResponse
from app.features.pedidos_forms.create.service import create_pedido_form
from app.features.pedidos_forms.get.service import get_pedidos_by_client
from app.features.pedidos_forms.signal.schemas import PedidoStatusUpdate
from app.features.pedidos_forms.signal.service import update_pedidos_status

router = APIRouter(prefix="/pedidos-forms", tags=["Pedidos Forms"])

@router.post("/", response_model=PedidoFormResponse, status_code=201)
async def create_pedido(data: PedidoFormCreate):
    """
    Endpoint público para que los clientes finales rellenen el formulario.
    Envía la la información del pedido a Google Sheets a través de Apps Script.
    """
    return await create_pedido_form(data)

@router.get("/")
async def get_pedidos(id_usuario: str):
    """
    Endpoint para consultar los pedidos realizados mediante el form.
    Permite a tu cliente ver su bandeja de pedidos en Sheets.
    TODO: En el futuro se recomienda extraer 'id_usuario' de las dependencias Token en lugar de parámetro query.
    """
    return await get_pedidos_by_client(id_usuario)

@router.patch("/señal-impreso")
async def signal_pedidos_impreso(data: PedidoStatusUpdate):
    """
    Recibe una señal por uno o varios pedidos.
    1. Realiza una tarea secundaria independiente (en service.py).
    2. Modifica la señal (estado) de los envíos en el Google Sheet a 'Impreso' (o el asignado).
    """
    result = await update_pedidos_status(
        pedidos_ids=data.pedidos_ids,
        nuevo_estado=data.nuevo_estado
    )
    return {
        "message": "Señal procesada: Tarea secundaria realizada y pedidos marcados con nuevo estado.", 
        "sheets_response": result
    }
