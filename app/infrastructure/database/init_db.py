from sqlalchemy.orm import Session

from app.infrastructure.database.base import Base
from app.infrastructure.database.seed import seed_database


def init_db(engine):

    Base.metadata.create_all(bind=engine)

    with Session(engine) as db:

        seed_database(db)
