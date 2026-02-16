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
        compania_id: str,
        case_type: str,
        priority: str,
        description: str,
    ) -> ExternalCaseResult:
        
        # Caso exitoso
        case_id = f"{compania_id}-{uuid.uuid4()}"

        return ExternalCaseResult(
            case_id=case_id,
            status="created",
            created=True,
        )
