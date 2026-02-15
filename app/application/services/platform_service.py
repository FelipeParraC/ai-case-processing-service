from app.infrastructure.connectors.mock_platform_connector import (
    MockPlatformConnector,
)

from app.domain.models.external_case_result import ExternalCaseResult


class PlatformService:

    def __init__(self):

        self.connector = MockPlatformConnector()


    def create_case(
        self,
        compania: str,
        case_type: str,
        priority: str,
        message: str,
    ) -> ExternalCaseResult:

        try:

            result = self.connector.create_case(
                compania,
                case_type,
                priority,
                message
            )

            return result

        except Exception:

            return None

