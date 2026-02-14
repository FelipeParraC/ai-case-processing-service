import uuid

from app.domain.models.external_case_result import ExternalCaseResult


class MockPlatformConnector:

    def create_case(
        self,
        company_code: str,
        classification: str,
        priority: str,
        message: str,
    ) -> ExternalCaseResult:

        case_id = f"{company_code}-{uuid.uuid4()}"

        return ExternalCaseResult(
            case_id=case_id,
            status="CREATED"
        )
