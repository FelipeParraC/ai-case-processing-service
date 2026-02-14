from pydantic import BaseModel
from typing import List


class ValidationResult(BaseModel):

    is_valid: bool

    missing_fields: List[str]

    errors: List[str]

    cleaned_message: str
