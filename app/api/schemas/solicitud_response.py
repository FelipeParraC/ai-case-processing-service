from pydantic import BaseModel
from datetime import date


class SolicitudResponse(BaseModel):

    compania: str

    solicitud_id: str

    solicitud_fecha: date

    solicitud_tipo: str

    solicitud_prioridad: str

    solicitud_id_cliente: str

    solicitud_tipo_id_cliente: str

    solicitud_id_plataforma_externa: str | None

    proximo_paso: str

    justificacion: str

    estado: str
