from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.infrastructure.database.dependencies import get_db
from app.infrastructure.repositories.admin_repository import AdminRepository

from app.api.schemas.admin_schemas import (
    CompaniaCreate,
    CompaniaResponse,
    CategoriaCreate,
    CategoriaResponse,
    ReglaCreate,
    ReglaResponse,
    SolicitudResponseAdmin,
    LogResponse,
)


router = APIRouter(prefix="/admin", tags=["Admin"])


# =====================================================
# GET
# =====================================================

@router.get("/companias", response_model=list[CompaniaResponse])
def get_companias(db: Session = Depends(get_db)):
    repo = AdminRepository(db)
    return repo.get_companias()


@router.get("/categorias", response_model=list[CategoriaResponse])
def get_categorias(db: Session = Depends(get_db)):
    repo = AdminRepository(db)
    return repo.get_categorias()


@router.get("/reglas", response_model=list[ReglaResponse])
def get_reglas(db: Session = Depends(get_db)):
    repo = AdminRepository(db)
    return repo.get_reglas()


@router.get("/solicitudes", response_model=list[SolicitudResponseAdmin])
def get_solicitudes(db: Session = Depends(get_db)):
    repo = AdminRepository(db)
    return repo.get_solicitudes()


@router.get("/logs", response_model=list[LogResponse])
def get_logs(db: Session = Depends(get_db)):
    repo = AdminRepository(db)
    return repo.get_logs()


# =====================================================
# POST
# =====================================================

@router.post("/companias", response_model=CompaniaResponse)
def create_compania(
    payload: CompaniaCreate,
    db: Session = Depends(get_db)
):
    repo = AdminRepository(db)
    return repo.create_compania(payload.model_dump())


@router.post("/categorias", response_model=CategoriaResponse)
def create_categoria(
    payload: CategoriaCreate,
    db: Session = Depends(get_db)
):
    repo = AdminRepository(db)
    return repo.create_categoria(payload.model_dump())


@router.post("/reglas", response_model=ReglaResponse)
def create_regla(
    payload: ReglaCreate,
    db: Session = Depends(get_db)
):
    repo = AdminRepository(db)
    return repo.create_regla(payload.model_dump())
