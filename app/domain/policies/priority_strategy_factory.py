from app.domain.interfaces.priority_strategy import PriorityStrategy
from app.domain.policies.rule_based_priority_strategy import (
    RuleBasedPriorityStrategy
)


class PriorityStrategyFactory:

    @staticmethod
    def get_strategy(company_code: str) -> PriorityStrategy:

        # aquí luego podremos agregar estrategias por empresa

        return RuleBasedPriorityStrategy()
