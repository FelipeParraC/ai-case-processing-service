import random
import time
import uuid

from app.core.config import settings
from app.domain.models.external_case_result import ExternalCaseResult


class ExternalPlatformError(Exception):
    pass


class MockPlatformConnector:

    def create_case(
        self,
        compania: str,
        case_type: str,
        priority: str,
        description: str,
    ) -> ExternalCaseResult:

        # Simular latencia
        latency = random.randint(
            settings.PLATFORM_LATENCY_MIN_MS,
            settings.PLATFORM_LATENCY_MAX_MS
        )

        time.sleep(latency / 1000)

        # Simular fallo
        if random.random() < settings.PLATFORM_FAILURE_RATE:

            raise ExternalPlatformError(
                "Simulated external platform failure"
            )

        # Caso exitoso
        case_id = f"{compania}-{uuid.uuid4()}"

        return ExternalCaseResult(
            case_id=case_id,
            status="created",
            created=True,
            latency_ms=latency
        )
