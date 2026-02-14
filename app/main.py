from fastapi import FastAPI

from app.core.config import settings
from app.infrastructure.database.init_db import init_db

from app.api.routes import cases


init_db()


app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
)


app.include_router(cases.router)


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}
