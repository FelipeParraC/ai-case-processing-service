from sqlalchemy.orm import Session

from app.domain.models.priority_result import PriorityResult
from app.infrastructure.repositories.rule_repository import RuleRepository
from app.infrastructure.connectors.external_priority_connector import ExternalPriorityConnector
from app.infrastructure.repositories.company_repository import CompanyRepository


class PriorityService:

    def __init__(self, db: Session):
        self.db = db
        self.rule_repo = RuleRepository(db)
        self.company_repo = CompanyRepository(db)
        self.external_connector = ExternalPriorityConnector()


    def determine_priority(
        self,
        company_id,
        message: str,
        case_type: str,
        extracted: dict | None = None
    ) -> PriorityResult:

        # Obtener objeto Company desde DB
        company = self.company_repo.get_by_id(company_id)

        if not company:
            return PriorityResult(
                level="Media",
                score=0.5,
                reason="Company no encontrada; prioridad por defecto."
            )

        company_name = (company.nombre or "").upper()

        # ===============================
        # External Priority Service
        # ===============================

        if company_name == "MENSAJERIA DEL VALLE":

            tipo_doc = (extracted or {}).get("tipo_documento", "")
            num_doc = (extracted or {}).get("numero_documento", "")

            data = self.external_connector.get_priority(
                tipo_documento=tipo_doc,
                numero_documento=num_doc,
                tipo_solicitud=case_type,
                descripcion=message,
            )

            prioridad = data.get("prioridad", "Media")
            reason = data.get(
                "reason",
                "Prioridad calculada por servicio externo."
            )

            return PriorityResult(
                level=prioridad,
                score=1.0,
                reason=reason
            )

        # ===============================
        # Default DB Rules
        # ===============================

        rule = self.rule_repo.get_rule_by_case_type(
            company_id,
            case_type
        )

        if rule:

            return PriorityResult(
                level=rule.priority,
                score=0.8,
                reason="Prioridad asignada por reglas de base de datos."
            )

        return PriorityResult(
            level="Media",
            score=0.5,
            reason="No hay regla específica; prioridad por defecto."
        )
