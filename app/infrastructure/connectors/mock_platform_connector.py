import uuid
import random
import time

from app.core.config import settings
from app.domain.models.external_case_result import ExternalCaseResult


class ExternalPlatformError(Exception):
    pass


class MockPlatformConnector:

    def __init__(self):

        self.failure_rate = getattr(
            settings,
            "PLATFORM_FAILURE_RATE",
            0.0
        )

        self.min_latency = 0.2
        self.max_latency = 0.8


    def create_case(
        self,
        compania: str,
        tipo: str,
        prioridad: str,
        descripcion: str,
    ) -> ExternalCaseResult:

        latency = random.uniform(
            self.min_latency,
            self.max_latency
        )

        time.sleep(latency)

        if random.random() < self.failure_rate:

            raise ExternalPlatformError(
                "Simulated external platform failure"
            )

        case_id = (
            f"{compania}-"
            f"{uuid.uuid4()}"
        )

        return ExternalCaseResult(
            case_id=case_id,
            success=True,
            latency_ms=int(latency * 1000),
        )
