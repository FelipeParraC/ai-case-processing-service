from sqlalchemy.orm import Session

from app.domain.models.priority_result import PriorityResult
from app.infrastructure.repositories.regla_repository import ReglaRepository


class RuleBasedPriorityStrategy:
    """
    Prioridad calculada usando reglas internas (tabla reglas).
    """

    def __init__(self, db: Session):
        self.db = db
        self.regla_repo = ReglaRepository(db)

    def calculate(
        self,
        compania_id,
        message: str,
        tipo_caso: str,
        extracted: dict | None = None,
    ) -> PriorityResult:
        regla = self.regla_repo.get_regla_by_tipo_caso(compania_id, tipo_caso)

        if regla:
            return PriorityResult(
                level=regla.prioridad,
                score=0.8,
                reason="Prioridad asignada por reglas de base de datos.",
            )

        return PriorityResult(
            level="Media",
            score=0.5,
            reason="No hay regla específica; prioridad por defecto.",
        )
