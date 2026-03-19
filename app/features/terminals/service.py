
from app.shared.http_client import HttpClient
from app.features.terminals.schemes import TerminalList
from app.features.process_shipment.auth.service import login

async def get_terminals() -> list[dict]:
    """
    Obtiene los terminales disponibles como origen y destino.
    Crea su propio cliente HTTP, inicia sesión y cierra al finalizar.
    """
    client = HttpClient()
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

    terminales = list((filter(lambda x: x['destino'] == 1, terminals)))
    
    terminales_ordenadas = list(map(lambda x: {'nombre': x['nombre'].title(), 'direccion': x['direccion'].title(), 'nombre_resumido': x['lugar_over']}, terminales))
    
    return terminales_ordenadas