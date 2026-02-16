from sqlalchemy.orm import Session

from app.domain.models.priority_result import PriorityResult
from app.infrastructure.connectors.external_priority_connector import ExternalPriorityConnector


class ExternalPriorityStrategy:
    """
    Prioridad calculada por un servicio externo (simulado o real),
    desacoplado del PriorityService.
    """

    def __init__(self, db: Session):
        self.db = db
        self.external_connector = ExternalPriorityConnector()

    def calculate(
        self,
        compania_id,
        message: str,
        tipo_caso: str,
        extracted: dict | None = None,
    ) -> PriorityResult:
        tipo_doc = (extracted or {}).get("tipo_documento", "")
        num_doc = (extracted or {}).get("numero_documento", "")

        data = self.external_connector.get_priority(
            tipo_documento=tipo_doc,
            numero_documento=num_doc,
            tipo_solicitud=tipo_caso,
            descripcion=message,
        )

        prioridad = data.get("prioridad", "Media")
        reason = data.get("reason", "Prioridad calculada por servicio externo.")

        return PriorityResult(
            level=prioridad,
            score=1.0,
            reason=reason,
        )
