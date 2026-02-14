from pydantic import BaseModel


class PriorityResult(BaseModel):

    level: str

    score: float

    reason: str
