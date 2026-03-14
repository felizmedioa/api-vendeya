# ============================================================================
# schemas.py — Modelos Pydantic para envíos
# ============================================================================

from typing import Optional

from pydantic import BaseModel


class TipoProductoJson(BaseModel):
    """Detalle del tipo de producto seleccionado."""
    value: int
    name: str
    detalle: str


class DatosEnvio(BaseModel):
    """
    Datos necesarios para crear un envío.

    Todos los campos obligatorios tienen su tipo definido.
    Los campos opcionales usan Optional con valor por defecto.
    """
    origen: int
    destino: int
    tipo_pago: str                          # "REMITENTE" o "DESTINATARIO"
    tipo_producto: int
    tipo_producto_json: TipoProductoJson
    cantidad: int
    peso: Optional[str] = ""
    alto: Optional[str] = ""
    largo: Optional[str] = ""
    ancho: Optional[str] = ""
    costo: float
    remitente: str                          # DNI del remitente
    destinatario: str                       # DNI del destinatario
    remitente_id: int
    destinatario_id: int
    garantia: int = 0
    garantia_costo: int = 0
    garantia_monto: str = "0.00"
    contacto_doc: Optional[str] = ""
    grrs: str = "[]"
    clave: str
    aereo: int = 0
    servicio_cobranza: int = 0
    servicio_cobranza_costo: int = 0
    servicio_cobranza_datos: str = '{"document":"","name":"","bank":"","type_account":"","account_number":"","cci":""}'
    declaracion_jurada: Optional[str] = ""
