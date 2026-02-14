from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import Rule


class RuleRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_active_rules(self, company_id, rule_type=None):

        stmt = select(Rule).where(
            Rule.company_id == company_id,
            Rule.is_active == True
        )

        if rule_type:
            stmt = stmt.where(Rule.rule_type == rule_type)

        result = self.db.execute(stmt)

        return result.scalars().all()


    def create(self, company_id, rule_type, config):

        rule = Rule(
            company_id=company_id,
            rule_type=rule_type,
            config=config
        )

        self.db.add(rule)

        self.db.commit()

        self.db.refresh(rule)

        return rule
