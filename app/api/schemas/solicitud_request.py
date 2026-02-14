from pydantic import BaseModel, Field


class SolicitudRequest(BaseModel):

    compania: str = Field(
        ...,
        description="Nombre de la compañía"
    )

    solicitud_id: str = Field(
        ...,
        description="ID de la solicitud"
    )

    solicitud_descripcion: str = Field(
        ...,
        description="Descripción de la solicitud"
    )
