from app.infrastructure.connectors.mock_platform_connector import (
    MockPlatformConnector,
    ExternalPlatformError,
)

from app.domain.models.external_case_result import ExternalCaseResult

import time


class PlatformService:

    def __init__(self):

        self.connector = MockPlatformConnector()

        self.max_retries = 3

        self.retry_delay = 0.5


    def create_case(
        self,
        compania,
        tipo,
        prioridad,
        descripcion,
    ) -> ExternalCaseResult | None:

        last_exception = None

        for attempt in range(self.max_retries):

            try:

                return self.connector.create_case(
                    compania,
                    tipo,
                    prioridad,
                    descripcion,
                )

            except ExternalPlatformError as e:

                last_exception = e

                time.sleep(self.retry_delay)

        return None
