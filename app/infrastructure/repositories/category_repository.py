from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import Category


class CategoryRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_by_company(self, company_id):

        stmt = select(Category).where(
            Category.company_id == company_id,
            Category.is_active == True
        )

        result = self.db.execute(stmt)

        return result.scalars().all()


    def create(self, company_id, name, description=None):

        category = Category(
            company_id=company_id,
            name=name,
            description=description
        )

        self.db.add(category)

        self.db.commit()

        self.db.refresh(category)

        return category
