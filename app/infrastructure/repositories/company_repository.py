from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.infrastructure.database.models import Company


class CompanyRepository:

    def __init__(self, db: Session):

        self.db = db


    def get_by_name_or_code(self, name_or_code: str) -> Company | None:

        return (

            self.db.query(Company)

            .filter(
                or_(
                    Company.nombre == name_or_code
                )
            )

            .first()

        )
