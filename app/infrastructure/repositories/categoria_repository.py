from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import Categoria


class CategoriaRepository:

    def __init__(self, db: Session):
        self.db = db


    def get_by_compania(self, compania_id):

        stmt = select(Categoria).where(
            Categoria.compania_id == compania_id,
            Categoria.activa == True
        )

        result = self.db.execute(stmt)

        return result.scalars().all()


    def create(self, compania_id, name, description=None):

        categoria = Categoria(
            compania_id=compania_id,
            name=name,
            description=description
        )

        self.db.add(categoria)

        self.db.commit()

        self.db.refresh(categoria)

        return categoria
