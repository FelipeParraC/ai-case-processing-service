from app.infrastructure.database.session import engine, Base
import time

def init_db():

    retries = 5

    for i in range(retries):
        try:
            Base.metadata.create_all(bind=engine)
            return
        except Exception:
            time.sleep(2)

    raise Exception("Database connection failed")
