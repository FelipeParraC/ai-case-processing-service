from pydantic import BaseModel


class ExternalCaseResult(BaseModel):

    case_id: str

    status: str
