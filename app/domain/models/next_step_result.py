from pydantic import BaseModel


class NextStepResult(BaseModel):

    action: str

    reason: str
