from app.infrastructure.connectors.mock_platform_connector import MockPlatformConnector, ExternalPlatformError
from app.core.config import settings

class PlatformService:
    def __init__(self):
        self.connector = MockPlatformConnector()

    def create_case(self, company: str, case_type: str, priority: str, message: str):
        attempts = settings.PLATFORM_RETRY_MAX_ATTEMPTS

        last_error = None
        for attempt in range(1, attempts + 1):
            try:
                return self.connector.create_case(company, case_type, priority, message)
            except ExternalPlatformError as e:
                last_error = str(e)
                # aquí puedes loggear con logger JSON si ya lo tienes
                if attempt == attempts:
                    break

        # ✅ fallback sin reventar endpoint
        return None
