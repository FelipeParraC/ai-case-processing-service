from sqlalchemy.orm import Session

from app.infrastructure.repositories.category_repository import CategoryRepository
from app.infrastructure.repositories.rule_repository import RuleRepository

from app.infrastructure.llm.llm_adapter import GroqLLMClient

from app.domain.models.llm_classification_result import LLMClassificationResult


class ClassificationService:

    def __init__(self, db: Session):

        self.db = db

        self.category_repo = CategoryRepository(db)

        self.rule_repo = RuleRepository(db)

        self.llm = GroqLLMClient()


    def classify(
        self,
        company_id,
        message
    ) -> LLMClassificationResult:

        # Obtener categorías válidas desde DB
        categories = self.category_repo.get_by_company(company_id)

        category_names = [c.name for c in categories]


        # Clasificación vía LLM
        llm_result = self.llm.classify_case(
            message,
            category_names
        )

        case_type = llm_result.case_type


        # Obtener regla desde DB
        rule = self.rule_repo.get_rule_by_case_type(
            company_id,
            case_type
        )


        # Justificación SIEMPRE desde DB si existe
        if rule and rule.justification_template:

            justification = rule.justification_template

        else:

            justification = llm_result.justification


        return LLMClassificationResult(

            case_type=case_type,

            justification=justification,

            confidence=(
                llm_result.confidence
                if hasattr(llm_result, "confidence")
                else 0.9
            )

        )
