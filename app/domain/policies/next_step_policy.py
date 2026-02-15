from app.infrastructure.repositories.rule_repository import RuleRepository
from app.domain.models.next_step_result import NextStepResult


class NextStepPolicy:

    def __init__(self, db):
        self.rule_repo = RuleRepository(db)


    def determine_next_step(
        self,
        company_id,
        case_type: str,
        priority_level: str
    ) -> NextStepResult:

        rule = self.rule_repo.get_rule_by_case_type(
            company_id,
            case_type
        )

        if rule and rule.next_step:

            return NextStepResult(
                action=rule.next_step,
                reason=f"Configurado en Rule DB para case_type='{case_type}'"
            )

        return NextStepResult(
            action="RESPUESTA_DIRECTA",
            reason="Fallback default policy"
        )
