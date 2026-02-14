from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import Company


class CompanyRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_by_code(self, code: str) -> Company | None:

        stmt = select(Company).where(
            Company.code == code,
            Company.is_active == True
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()


    def get_by_id(self, company_id):

        stmt = select(Company).where(
            Company.id == company_id
        )

        result = self.db.execute(stmt)

        return result.scalar_one_or_none()


    def create(self, name: str, code: str) -> Company:

        company = Company(
            name=name,
            code=code
        )

        self.db.add(company)

        self.db.commit()

        self.db.refresh(company)

        return company


    def list_all(self):

        stmt = select(Company)

        result = self.db.execute(stmt)

        return result.scalars().all()
