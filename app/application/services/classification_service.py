from sqlalchemy.orm import Session

from app.infrastructure.repositories.category_repository import CategoryRepository
from app.infrastructure.llm.llm_adapter import GroqLLMClient


class ClassificationService:

    def __init__(self, db: Session):

        self.db = db

        self.category_repo = CategoryRepository(db)

        self.llm = GroqLLMClient()


    def classify(self, company_id, message):

        categories = self.category_repo.get_by_company(company_id)

        category_names = [c.name for c in categories]

        result = self.llm.classify_case(
            message,
            category_names
        )

        return result
