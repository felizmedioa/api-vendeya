from fastapi import APIRouter, Depends
from app.core.dependencies import get_shalom_client
from app.shared.http_client import ShalomHttpClient

from app.features.terminals.service import get_terminals, filter_terminals

from app.features.terminals.schemes import TerminalList

router = APIRouter(
    tags=["Obtener Terminales"],
)

@router.get(
    "/terminals",
    summary="Obtener terminales del API",
    description="Obtener terminales disponibles como origen y destino",
)
async def obtener_terminales(
    client: ShalomHttpClient = Depends(get_shalom_client),
) -> list[dict]:

    terminales_unfiltered = await get_terminals(client)
    return filter_terminals(terminales_unfiltered)
