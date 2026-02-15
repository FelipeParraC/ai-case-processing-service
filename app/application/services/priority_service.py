from app.infrastructure.repositories.rule_repository import RuleRepository
from app.domain.models.priority_result import PriorityResult


class PriorityService:

    def __init__(self, db):
        self.db = db


    def determine_priority(
        self,
        company_id,
        message: str,
        case_type: str,
    ) -> PriorityResult:

        rule_repo = RuleRepository(self.db)

        rule = rule_repo.get_rule_by_case_type(
            company_id,
            case_type
        )

        if not rule:

            return PriorityResult(
                level="Media",
                score=0.5,
                reason="Prioridad por defecto (sin regla configurada)"
            )


        message_lower = message.lower()

        for keyword in rule.keywords:

            if keyword.lower() in message_lower:

                return PriorityResult(
                    level=rule.priority,
                    score=0.95,
                    reason=f"Keyword detectada: '{keyword}'"
                )


        return PriorityResult(
            level=rule.priority,
            score=0.6,
            reason="Prioridad definida por regla de tipo de caso"
        )
