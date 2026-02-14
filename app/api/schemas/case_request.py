from pydantic import BaseModel, Field
from typing import Optional, Dict


class CaseProcessRequest(BaseModel):

    company_code: str = Field(
        ...,
        description="Código de la empresa"
    )

    message: str = Field(
        ...,
        description="Mensaje del cliente"
    )

    metadata: Optional[Dict] = Field(
        default_factory=dict
    )
