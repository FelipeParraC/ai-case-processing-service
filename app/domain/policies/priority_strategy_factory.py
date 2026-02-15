from app.domain.policies.rule_based_priority_strategy import (
    RuleBasedPriorityStrategy
)
from app.domain.policies.external_priority_strategy import (
    ExternalPriorityStrategy
)



class PriorityStrategyFactory:

    @staticmethod
    def get_strategy(self, company_name: str):

        if company_name.upper() == "MENSAJERIA DEL VALLE":

            return ExternalPriorityStrategy()

        return RuleBasedPriorityStrategy(self.db)

