from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import SolicitudRecord


class SolicitudRepository:

    def __init__(self, db: Session):
        self.db = db


    def get(
        self,
        company_id,
        solicitud_id: str
    ) -> SolicitudRecord | None:

        stmt = select(SolicitudRecord).where(
            SolicitudRecord.company_id == company_id,
            SolicitudRecord.solicitud_id == solicitud_id,
        )

        return self.db.execute(stmt).scalar_one_or_none()


    def create(
        self,
        company_id,
        solicitud_id,
        request_id,
        status,
        external_case_id,
        response_json,
    ) -> SolicitudRecord:

        record = SolicitudRecord(
            company_id=company_id,
            solicitud_id=solicitud_id,
            request_id=request_id,
            status=status,
            external_case_id=external_case_id,
            response_json=response_json,
        )

        self.db.add(record)

        self.db.commit()

        self.db.refresh(record)

        return record
