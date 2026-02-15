from sqlalchemy.orm import Session
from sqlalchemy import select, func

from app.infrastructure.database.models import Company


class CompanyRepository:

    def __init__(self, db: Session):
        self.db = db


    # ===============================
    # Buscar por ID (usado en PriorityService)
    # ===============================

    def get_by_id(self, company_id):

        stmt = select(Company).where(
            Company.id == company_id
        )

        return self.db.execute(stmt).scalar_one_or_none()


    # ===============================
    # Buscar por nombre o código
    # (usado en endpoint principal)
    # ===============================

    def get_by_name_or_code(self, value: str):

        normalized = value.strip().upper()

        stmt = select(Company).where(
            func.upper(Company.nombre) == normalized
        )

        return self.db.execute(stmt).scalar_one_or_none()
