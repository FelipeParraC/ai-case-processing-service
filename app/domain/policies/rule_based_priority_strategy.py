from app.domain.interfaces.priority_strategy import PriorityStrategy
from app.domain.models.priority_result import PriorityResult


class RuleBasedPriorityStrategy(PriorityStrategy):

    HIGH_PRIORITY_KEYWORDS = [
        "siniestro",
        "urgente",
        "fraude",
        "robo",
        "accidente",
    ]

    MEDIUM_PRIORITY_KEYWORDS = [
        "problema",
        "error",
        "reclamo",
    ]


    def determine_priority(
        self,
        message: str,
        classification: str,
        metadata: dict | None = None,
    ) -> PriorityResult:

        text = message.lower()

        for keyword in self.HIGH_PRIORITY_KEYWORDS:

            if keyword in text:

                return PriorityResult(
                    level="HIGH",
                    score=0.9,
                    reason=f"Detected high-priority keyword: {keyword}"
                )

        for keyword in self.MEDIUM_PRIORITY_KEYWORDS:

            if keyword in text:

                return PriorityResult(
                    level="MEDIUM",
                    score=0.6,
                    reason=f"Detected medium-priority keyword: {keyword}"
                )

        return PriorityResult(
            level="LOW",
            score=0.3,
            reason="No priority keywords detected"
        )
