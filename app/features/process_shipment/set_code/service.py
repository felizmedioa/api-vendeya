# ============================================================================
# service.py — Lógica de set_code + generación de códigos + Pushover
# ============================================================================

from app.features.process_shipment.set_code.schemas import SetCodeRequest
from app.shared.http_client import HttpClient
import random
import httpx


async def set_code(client: HttpClient, datos: SetCodeRequest):

    client.verificar_sesion()
    headers = client.obtener_headers_ajax()

    response = await client.client.post(
        "/security-code/massive",
        headers=headers,
        json=datos.model_dump(),
    )

    return response.json()


def generate_code(previous_code: str = "") -> str:
    """
    Genera un código de 4 dígitos que cumple:
      1. No todos los dígitos iguales  (ej: 1111, 5555)
      2. No secuencia consecutiva asc/desc (ej: 1234, 9876)
      3. Diferente al código anterior
    """
    while True:
        code = str(random.randint(1000, 9999))

        # Regla 1: no todos iguales
        if len(set(code)) == 1:
            continue

        # Regla 2: no consecutivos ascendentes ni descendentes
        digits = [int(d) for d in code]
        diffs = [digits[i + 1] - digits[i] for i in range(len(digits) - 1)]
        if diffs == [1, 1, 1] or diffs == [-1, -1, -1]:
            continue

        # Regla 3: diferente al anterior
        if code == previous_code:
            continue

        return code


async def send_pushover_notification(code: str) -> dict:
    """
    Envía una notificación a Pushover con el nuevo código diario.
    Tokens hardcoded según preferencia del proyecto.
    """
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.pushover.net/1/messages.json",
            json={
                "token": "a7cktd4uy585kpcaqdq96ukua9rpgp",
                "user": "uc4s3r8tb8uu24v7xef9qcrypew3ep",
                "message": f"🔐 Nuevo código diario: {code}",
            },
        )
        return response.json()


async def send_shipment_pushover_notification(
    telefono: str,
    dni: str,
    clave_paquete: str,
    success: bool,
    error_detail: str | None = None,
) -> dict:
    """
    Envía una notificación Pushover con el resultado del registro de un paquete.
    Se envía tanto en éxito como en error.
    """
    if success:
        message = (
            f"✅ Paquete registrado exitosamente\n"
            f"• Número: {telefono}\n"
            f"• DNI: {dni}\n"
            f"• Clave: {clave_paquete}"
        )
    else:
        message = (
            f"❌ Error al registrar paquete\n"
            f"• Número: {telefono}\n"
            f"• DNI: {dni}\n"
            f"• Clave: {clave_paquete}\n"
            f"• Error: {error_detail}"
        )

    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://api.pushover.net/1/messages.json",
            json={
                "token": "av5addzfqxjwxy5r8vi45xdb3pnoju",
                "user": "u1rrniu5yy9xfcugs3o3kuz8ofn6fa",
                "message": message,
            },
        )
        return response.json()