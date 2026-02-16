import time
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from app.core.logger import get_logger


logger = get_logger("middleware")


class RequestTracingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
        request.state.request_id = request_id

        start = time.time()

        response: Response = await call_next(request)

        latency_ms = int((time.time() - start) * 1000)

        response.headers["X-Request-Id"] = request_id

        logger.info(
            "request_completed",
            extra={
                "extra": {
                    "request_id": request_id,
                    "path": str(request.url.path),
                    "method": request.method,
                    "status_code": response.status_code,
                    "latency_ms": latency_ms,
                }
            }
        )

        return response
