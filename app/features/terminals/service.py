
from app.shared.http_client import ShalomHttpClient
from app.features.terminals.schemes import TerminalList

async def get_terminals(
    client: ShalomHttpClient,
) -> list[dict]:
    """
    Obtiene los terminales disponibles como origen y destino.
    """
    client.verificar_sesion()
    headers = client.obtener_headers_ajax()

    response = await client.client.post(
        "/envia_ya/terminals",
        headers=headers,
    )

    return response.json()['Map']

def filter_terminals(terminals: list[dict]):

    terminales = list((filter(lambda x: x['destino'] == 1 and x['departamento'] != 'LIMA' and x['provincia'] != 'LIMA', terminals)))
    
    terminales_ordenadas = list(map(lambda x: {'id': x['ter_id'], 'nombre': x['nombre'], 'nombre_resumido': x['lugar_over']}, terminales))
    
    return terminales_ordenadas