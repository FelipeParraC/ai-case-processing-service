from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter(prefix="/mock/mensajeria-del-valle", tags=["Mock Services"])


class PriorityRequest(BaseModel):

    tipo_documento: str
    numero_documento_cliente: str
    tipo_solicitud: str


class PriorityResponse(BaseModel):

    prioridad: str
    reason: str


@router.post("/prioridad", response_model=PriorityResponse)
def determinar_prioridad(req: PriorityRequest):

    tipo = req.tipo_solicitud.lower()

    numero = req.numero_documento_cliente

    # Regla 1 — Incidentes críticos
    if any(word in tipo for word in ["robo", "perdido", "nunca llegó", "extraviado"]):

        return PriorityResponse(
            prioridad="Alta",
            reason="Incidente crítico de entrega."
        )

    # Regla 2 — Clientes VIP simulados
    if numero.endswith("999"):

        return PriorityResponse(
            prioridad="Alta",
            reason="Cliente VIP."
        )

    # Regla 3 — Consultas
    if any(word in tipo for word in ["consulta", "información"]):

        return PriorityResponse(
            prioridad="Baja",
            reason="Consulta informativa."
        )

    # Regla 4 — Default con ligera variabilidad
    prioridad = random.choices(
        ["Media", "Media", "Media", "Alta", "Baja"],
        weights=[60, 10, 10, 10, 10],
        k=1
    )[0]

    return PriorityResponse(
        prioridad=prioridad,
        reason="Prioridad determinada por reglas del sistema externo."
    )
