from sqlalchemy.orm import Session

from app.infrastructure.database.models import Company, Category


def seed_database(db: Session):

    existing = db.query(Company).first()

    if existing:
        return

    # Crear empresa de prueba

    company = Company(
        name="Seguros Bolívar Demo",
        code="BOLIVAR"
    )

    db.add(company)

    db.commit()

    db.refresh(company)

    # Crear categorías de prueba

    categories = [
        Category(
            company_id=company.id,
            name="CLAIM",
            description="Insurance claim"
        ),
        Category(
            company_id=company.id,
            name="COMPLAINT",
            description="Customer complaint"
        ),
        Category(
            company_id=company.id,
            name="INQUIRY",
            description="Customer inquiry"
        ),
    ]

    db.add_all(categories)

    db.commit()

    print("Database seeded successfully")
