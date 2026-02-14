from app.infrastructure.database.session import engine, Base
import app.infrastructure.database.models


def init_db():
    Base.metadata.create_all(bind=engine)
