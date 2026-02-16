from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.json_utils import to_json_serializable
from app.infrastructure.database.models import Solicitud


class SolicitudRepository:

    def __init__(self, db: Session):
        self.db = db

    # ===============================
    # Obtener solicitud (idempotencia)
    # ===============================

    def get(
        self,
        compania_id,
        solicitud_id: str,
    ) -> Solicitud | None:

        stmt = select(Solicitud).where(
            Solicitud.compania_id == compania_id,
            Solicitud.solicitud_id == solicitud_id,
        )

        return self.db.execute(stmt).scalar_one_or_none()

    # ===============================
    # Crear solicitud
    # ===============================

    def create(
        self,
        compania_id,
        solicitud_id: str,
        id_request: str,
        estado: str,
        id_caso_externo: str | None,
        respuesta_json: dict,
    ) -> Solicitud:

        solicitud = Solicitud(
            compania_id=compania_id,
            solicitud_id=solicitud_id,
            id_request=id_request,
            estado=estado,
            id_caso_externo=id_caso_externo,
            respuesta_json=to_json_serializable(respuesta_json),
        )

        self.db.add(solicitud)

        self.db.commit()

        self.db.refresh(solicitud)

        return solicitud
