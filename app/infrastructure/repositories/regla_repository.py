from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import Regla


class ReglaRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_reglas_by_compania(
        self,
        compania_id,
    ) -> list[Regla]:

        stmt = select(Regla).where(
            Regla.compania_id == compania_id
        )

        return list(
            self.db.execute(stmt).scalars().all()
        )


    def get_regla_by_tipo_caso(
        self,
        compania_id,
        tipo_caso: str,
    ) -> Regla | None:

        stmt = select(Regla).where(
            Regla.compania_id == compania_id,
            Regla.tipo_caso == tipo_caso,
        )

        return self.db.execute(stmt).scalar_one_or_none()
