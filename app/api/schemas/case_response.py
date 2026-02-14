from pydantic import BaseModel
from typing import Optional, Dict


class CaseProcessResponse(BaseModel):

    request_id: str

    status: str

    company_found: bool

    message: str

    metadata: Optional[Dict] = None
