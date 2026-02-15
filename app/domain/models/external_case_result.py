from pydantic import BaseModel

class ExternalCaseResult(BaseModel):
    case_id: str
    status: str
    success: bool = True
    latency_ms: int | None = None
