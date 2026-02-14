from fastapi import FastAPI

app = FastAPI(
    title="AI Case Processing Service",
    version="1.0.0",
    description="Microservicio de procesamiento inteligente de casos"
)


@app.get("/health/live")
def live():
    return {"status": "alive"}


@app.get("/health/ready")
def ready():
    return {"status": "ready"}
