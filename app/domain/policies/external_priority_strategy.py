import random

from app.domain.models.priority_result import PriorityResult


class ExternalPriorityStrategy:

    def determine(
        self,
        compania,
        mensaje,
        tipo,
    ) -> PriorityResult:

        priority = random.choice(
            ["Alta", "Media", "Baja"]
        )

        return PriorityResult(
            level=priority,
            score=0.9,
            reason="Prioridad determinada por servicio externo"
        )
