# ============================================================================
# service.py — Lógica para creación de un pedido por formulario
# ============================================================================

import logging
import datetime

import httpx
from fastapi import HTTPException

from app.core.config import settings
from app.features.pedidos_forms.create.schemas import PedidoFormCreate

logger = logging.getLogger("pedidos_forms.create")


async def create_pedido_form(datos: PedidoFormCreate) -> dict:
    """
    Inscribe un nuevo pedido en Google Sheets proveniente del formulario.

    Flujo:
    1. Autogenerar datos faltantes (ID pedido, fecha, estado inicial)
    2. Construir el payload con la acción 'create_pedido'
    3. Enviar los datos a Google Apps Script
    4. Retornar el pedido generado
    """

    # ── Paso 1: Autogenerar datos faltantes ──────────────────────────
    now = datetime.datetime.now()
    fecha = now.strftime("%d/%m/%Y")
    timestamp = now.isoformat()
    estado = "Pendiente"
    
    # ── Paso 2: Preparar el payload ──────────────────────────────────
    payload = {
        "action": "create_pedido",
        "id_usuario": datos.id_usuario,
        "agencia": datos.agencia,
        "nombre_completo": datos.nombre_completo,
        "dni": datos.dni,
        "telefono": datos.telefono,
        "destino": datos.destino,
        "direccion": datos.direccion,
        "estado": estado,
        "fecha": fecha,
        "timestamp": timestamp
    }
    
    # ── Paso 3: Consultar Google Apps Script ─────────────────────────
    try:
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                settings.APPS_SCRIPT_PEDIDOS_FORMS_URL,
                json=payload,
                follow_redirects=True,
            )
    except httpx.RequestError as exc:
        logger.error(f"Error de red al crear el pedido: {exc}")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    if response.status_code != 200:
        logger.error(
            f"Google Script respondió con status {response.status_code}"
        )
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    try:
        data = response.json()
    except Exception:
        logger.error("Respuesta de Google Script no es JSON válido")
        raise HTTPException(
            status_code=500,
            detail="Error interno del servidor.",
        )

    # ── Paso 4: Interpretar la respuesta ─────────────────────────────
    status = data.get("status", "").lower()

    if status == "error":
        raise HTTPException(
            status_code=400,
            detail=data.get("message", "Error al crear el pedido en Google Sheets"),
        )
        
    # Añadimos el id_pedido secuencial generado por el Apps Script al payload devuelto
    payload["id_pedido"] = data.get("id_pedido", "PED-UNKNOWN")
        
    return payload
