from fastapi import APIRouter

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
async def obtener_terminales() -> list[dict]:

    terminales_unfiltered = await get_terminals()
    return filter_terminals(terminales_unfiltered)
