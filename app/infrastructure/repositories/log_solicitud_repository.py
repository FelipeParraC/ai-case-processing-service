from sqlalchemy.orm import Session

from app.infrastructure.database.models import LogSolicitud

from app.core.json_utils import to_json_serializable


class LogSolicitudRepository:

    def __init__(self, db: Session):
        self.db = db


    def create(
        self,
        id_request,
        compania_id,
        estado,
        latencia_ms=None,
        codigo_error=None,
        detalle_error=None,
    ):
        try:
            log = LogSolicitud(
                id_request=id_request,
                compania_id=compania_id,
                estado=estado,
                latencia_ms=latencia_ms,
                codigo_error=codigo_error,
                detalle_error=to_json_serializable(detalle_error) if detalle_error else None,
            )

            self.db.add(log)

            self.db.commit()

            self.db.refresh(log)

            return log
        
        except Exception as e:
            
            self.db.rollback()
            raise e