from sqlalchemy.orm import Session

from app.domain.policies.external_priority_strategy import ExternalPriorityStrategy
from app.domain.policies.rule_based_priority_strategy import RuleBasedPriorityStrategy
from app.infrastructure.repositories.compania_repository import CompaniaRepository


class PriorityStrategyFactory:
    """
    Decide qué estrategia usar para calcular prioridad, basado en configuración
    de la compañía en DB (NO hardcode por nombre).
    """

    def __init__(self, db: Session):
        self.db = db
        self.compania_repo = CompaniaRepository(db)

    def get_strategy(self, compania_id):
        compania = self.compania_repo.get_by_id(compania_id)

        # Fail-safe: si no existe compañía, usar reglas internas (o default)
        if not compania:
            return RuleBasedPriorityStrategy(self.db)

        if getattr(compania, "usa_servicio_prioridad_externo", False):
            return ExternalPriorityStrategy(self.db)

        return RuleBasedPriorityStrategy(self.db)
