import time

from app.infrastructure.database.session import engine, Base, SessionLocal
import app.infrastructure.database.models

from app.infrastructure.database.seed import seed_database


def init_db():

    retries = 5

    for _ in range(retries):

        try:

            Base.metadata.create_all(bind=engine)

            db = SessionLocal()

            seed_database(db)

            db.close()

            return

        except Exception:

            time.sleep(2)

    raise Exception("Database initialization failed")
