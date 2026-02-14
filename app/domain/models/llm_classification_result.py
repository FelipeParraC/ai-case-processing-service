from pydantic import BaseModel


class LLMClassificationResult(BaseModel):

    case_type: str

    confidence: float

    justification: str
