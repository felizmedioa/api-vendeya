
from app.shared.http_client import ShalomHttpClient
from app.features.terminals.schemes import TerminalList
from app.features.process_shipment.auth.service import login

async def get_terminals() -> list[dict]:
    """
    Obtiene los terminales disponibles como origen y destino.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = ShalomHttpClient()
    try:
        await login(client)
        headers = client.obtener_headers_ajax()

        response = await client.client.post(
            "/envia_ya/terminals",
            headers=headers,
        )

        return response.json()['Map']
    finally:
        await client.close()

def filter_terminals(terminals: list[dict]):

    terminales = list((filter(lambda x: x['destino'] == 1 and x['departamento'] != 'LIMA' and x['provincia'] != 'LIMA', terminals)))
    
    terminales_ordenadas = list(map(lambda x: {'id': x['ter_id'], 'nombre': x['nombre'], 'nombre_resumido': x['lugar_over']}, terminales))
    
    return terminales_ordenadas