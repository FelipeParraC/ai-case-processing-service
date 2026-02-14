from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0",
    description="Microservicio de procesamiento inteligente de casos"
)


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {
        "status": "ready",
        "environment": settings.APP_ENV
    }
