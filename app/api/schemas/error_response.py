from pydantic import BaseModel
from typing import Optional, Dict, Any


class ErrorResponse(BaseModel):

    request_id: str
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
