from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import Rule


class RuleRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_rules_for_company(
        self,
        company_id,
    ) -> list[Rule]:

        stmt = select(Rule).where(
            Rule.compania_id == company_id
        )

        return list(
            self.db.execute(stmt).scalars().all()
        )


    def get_rule_by_case_type(
        self,
        company_id,
        case_type: str,
    ) -> Rule | None:

        stmt = select(Rule).where(
            Rule.compania_id == company_id,
            Rule.case_type == case_type,
        )

        return self.db.execute(stmt).scalar_one_or_none()
