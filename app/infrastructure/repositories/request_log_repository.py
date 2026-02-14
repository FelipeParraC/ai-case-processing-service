from sqlalchemy.orm import Session

from app.infrastructure.database.models import RequestLog


class RequestLogRepository:

    def __init__(self, db: Session):
        self.db = db


    def create(
        self,
        request_id,
        company_id,
        status,
        latency_ms=None,
        error_code=None,
        error_detail=None,
    ):

        log = RequestLog(
            request_id=request_id,
            company_id=company_id,
            status=status,
            latency_ms=latency_ms,
            error_code=error_code,
            error_detail=error_detail,
        )

        self.db.add(log)

        self.db.commit()

        self.db.refresh(log)

        return log
