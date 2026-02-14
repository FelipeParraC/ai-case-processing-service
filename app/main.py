from fastapi import FastAPI, HTTPException

from app.core.errors import http_exception_handler, unhandled_exception_handler
from app.core.config import settings
from app.core.middleware import RequestTracingMiddleware

from app.infrastructure.database.init_db import init_db

from app.api.routes import solicitudes


init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)

app.add_middleware(RequestTracingMiddleware)

app.include_router(solicitudes.router)

app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)



@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}
