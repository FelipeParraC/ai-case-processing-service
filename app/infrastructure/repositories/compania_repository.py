from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.infrastructure.database.models import Compania


class CompaniaRepository:

    def __init__(self, db: Session):
        self.db = db


    # ===============================
    # Buscar por ID (usado en PriorityService)
    # ===============================

    def get_by_id(self, compania_id):

        stmt = select(Compania).where(
            Compania.id == compania_id
        )

        return self.db.execute(stmt).scalar_one_or_none()


    # ===============================
    # Buscar por nombre o código
    # (usado en endpoint principal)
    # ===============================

    def get_by_nombre(self, value: str):

        normalized = value.strip().upper()

        stmt = select(Compania).where(
            func.upper(Compania.nombre) == normalized
        )

        return self.db.execute(stmt).scalar_one_or_none()
