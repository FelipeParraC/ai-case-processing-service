from sqlalchemy.orm import Session

from app.infrastructure.database.models import Company, Category, Rule


def seed_database(db: Session):

    companies_data = [

        {
            "nombre": "GASES DEL ORINOCO",

            "categories": [
                "Incidente técnico",
                "Consulta",
                "Queja",
                "Solicitud administrativa",
            ],

            "rules": [

                {
                    "case_type": "Incidente técnico",

                    "keywords": [
                        "estufa",
                        "gas",
                        "falla",
                        "no funciona",
                        "urgente",
                        "riesgo"
                    ],

                    "priority": "HIGH",

                    "next_step": "CREATE_EXTERNAL_CASE",

                    "justification_template":
                        "Se detecta falla técnica en estufa de gas que requiere intervención presencial (delegación externa)."
                },

                {
                    "case_type": "Consulta",

                    "keywords": [
                        "consulta",
                        "información",
                        "pregunta"
                    ],

                    "priority": "LOW",

                    "next_step": "QUEUE_FOR_REVIEW",

                    "justification_template":
                        "Solicitud informativa que puede resolverse internamente."
                }

            ]
        },

        {
            "nombre": "MENSAJERIA DEL VALLE",

            "categories": [
                "Problema de entrega",
                "Consulta",
                "Queja",
            ],

            "rules": [

                {
                    "case_type": "Problema de entrega",

                    "keywords": [
                        "entrega",
                        "paquete",
                        "no llegó",
                        "retraso"
                    ],

                    "priority": "MEDIUM",

                    "next_step": "QUEUE_FOR_REVIEW",

                    "justification_template":
                        "Incidente relacionado con logística de entrega."
                }

            ]
        }

    ]

    for company_data in companies_data:

        nombre = company_data["nombre"]

        existing = db.query(Company).filter_by(nombre=nombre).first()

        if existing:

            company = existing

        else:

            company = Company(
                nombre=nombre
            )

            db.add(company)

            db.flush()

        # Categories

        for category_name in company_data["categories"]:

            exists_category = (
                db.query(Category)
                .filter_by(
                    company_id=company.id,
                    name=category_name
                )
                .first()
            )

            if not exists_category:

                category = Category(
                    company_id=company.id,
                    name=category_name,
                    is_active=True
                )

                db.add(category)

        # Rules

        for rule_data in company_data["rules"]:

            exists_rule = (
                db.query(Rule)
                .filter_by(
                    compania_id=company.id,
                    case_type=rule_data["case_type"]
                )
                .first()
            )

            if not exists_rule:

                rule = Rule(

                    compania_id=company.id,

                    case_type=rule_data["case_type"],

                    keywords=rule_data["keywords"],

                    priority=rule_data["priority"],

                    next_step=rule_data["next_step"],

                    justification_template=
                        rule_data["justification_template"]
                )

                db.add(rule)

    db.commit()

    print("Database seeded successfully")
