from app.infrastructure.connectors.mock_platform_connector import MockPlatformConnector, ExternalPlatformError
from app.core.config import settings

class PlatformService:
    def __init__(self):
        self.connector = MockPlatformConnector()

    def create_case(self, compania_id: str, case_type: str, priority: str, message: str):
        return self.connector.create_case(compania_id, case_type, priority, message)