from app.domain.models.next_step_result import NextStepResult


class NextStepPolicy:

    def determine_next_step(
        self,
        priority_level: str,
        classification: str,
        metadata: dict | None = None,
    ) -> NextStepResult:

        if priority_level == "HIGH":

            return NextStepResult(
                action="ESCALATE_IMMEDIATELY",
                reason="High priority case requires immediate escalation"
            )

        if priority_level == "MEDIUM":

            return NextStepResult(
                action="CREATE_EXTERNAL_CASE",
                reason="Medium priority case should be processed externally"
            )

        return NextStepResult(
            action="QUEUE_FOR_REVIEW",
            reason="Low priority case queued for manual review"
        )
