from sqlalchemy.orm import Session

from app.domain.models.priority_result import PriorityResult
from app.domain.policies.priority_strategy_factory import PriorityStrategyFactory


class PriorityService:
    """
    Servicio de aplicación que delega el cálculo de prioridad
    a una estrategia (interna o externa) decidida por la Factory.
    """

    def __init__(self, db: Session):
        self.db = db
        self.factory = PriorityStrategyFactory(db)

    def determine_priority(
        self,
        compania_id,
        message: str,
        tipo_caso: str,
        extracted: dict | None = None,
    ) -> PriorityResult:
        strategy = self.factory.get_strategy(compania_id)

        return strategy.calculate(
            compania_id=compania_id,
            message=message,
            tipo_caso=tipo_caso,
            extracted=extracted,
        )
