from sqlalchemy.orm import Session
from sqlalchemy import select

from app.infrastructure.database.models import (
    Compania,
    Categoria,
    Regla,
    Solicitud,
    LogSolicitud
)


class AdminRepository:

    def __init__(self, db: Session):
        self.db = db

    # =====================================================
    # COMPANIAS
    # =====================================================

    def get_companias(self):
        return list(self.db.execute(select(Compania)).scalars().all())

    def create_compania(self, data: dict):
        obj = Compania(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj


    # =====================================================
    # CATEGORIAS
    # =====================================================

    def get_categorias(self):
        return list(self.db.execute(select(Categoria)).scalars().all())

    def create_categoria(self, data: dict):
        obj = Categoria(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj


    # =====================================================
    # REGLAS
    # =====================================================

    def get_reglas(self):
        return list(self.db.execute(select(Regla)).scalars().all())

    def create_regla(self, data: dict):
        obj = Regla(**data)
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj


    # =====================================================
    # SOLICITUDES
    # =====================================================

    def get_solicitudes(self):
        return list(self.db.execute(select(Solicitud)).scalars().all())


    # =====================================================
    # LOGS
    # =====================================================

    def get_logs(self):
        return list(self.db.execute(select(LogSolicitud)).scalars().all())
