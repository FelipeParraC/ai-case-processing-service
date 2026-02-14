from app.infrastructure.connectors.mock_platform_connector import (
    MockPlatformConnector
)


class PlatformService:

    def __init__(self):

        self.connector = MockPlatformConnector()


    def create_case(
        self,
        company_code,
        classification,
        priority,
        message,
    ):

        return self.connector.create_case(
            company_code,
            classification,
            priority,
            message
        )
