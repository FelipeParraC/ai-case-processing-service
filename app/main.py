from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.core.errors import http_exception_handler, unhandled_exception_handler
from app.core.config import settings
from app.core.middleware import RequestTracingMiddleware

from app.infrastructure.database.init_db import init_db
from app.infrastructure.database.session import engine

from app.api.routes import solicitudes
from app.api.routes import mock_services


# Lifespan handler moderno
@asynccontextmanager
async def lifespan(app: FastAPI):

    # Startup
    init_db(engine)

    yield

    # Shutdown (opcional)
    # Aquí podrías cerrar conexiones, pools, etc.


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    lifespan=lifespan,
)


# Middleware
app.add_middleware(RequestTracingMiddleware)


# Routers
app.include_router(solicitudes.router)
app.include_router(mock_services.router)


# Exception handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(Exception, unhandled_exception_handler)


# Health checks
@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}
