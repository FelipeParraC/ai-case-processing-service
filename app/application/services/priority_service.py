from app.domain.policies.priority_strategy_factory import (
    PriorityStrategyFactory
)


class PriorityService:

    def determine_priority(
        self,
        company_code: str,
        message: str,
        classification: str,
        metadata: dict | None = None,
    ):

        strategy = PriorityStrategyFactory.get_strategy(
            company_code
        )

        return strategy.determine_priority(
            message,
            classification,
            metadata
        )
