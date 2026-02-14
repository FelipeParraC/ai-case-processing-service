from abc import ABC, abstractmethod

from app.domain.models.priority_result import PriorityResult


class PriorityStrategy(ABC):

    @abstractmethod
    def determine_priority(
        self,
        message: str,
        classification: str,
        metadata: dict | None = None,
    ) -> PriorityResult:

        pass
