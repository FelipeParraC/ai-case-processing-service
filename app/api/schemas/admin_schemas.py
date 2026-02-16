from datetime import datetime
from uuid import UUID
from typing import List, Optional

from pydantic import BaseModel, Field


# =====================================================
# COMPANIAS
# =====================================================

class CompaniaCreate(BaseModel):

    nombre: str = Field(..., example="NUEVA EMPRESA")

    usa_servicio_prioridad_externo: bool = False

    activa: bool = True


class CompaniaResponse(BaseModel):

    id: UUID

    nombre: str

    usa_servicio_prioridad_externo: bool

    activa: bool

    creada_en: datetime


# =====================================================
# CATEGORIAS
# =====================================================

class CategoriaCreate(BaseModel):

    compania_id: UUID

    nombre: str

    descripcion: Optional[str] = None

    activa: bool = True


class CategoriaResponse(BaseModel):

    id: UUID

    compania_id: UUID

    nombre: str

    descripcion: Optional[str]

    activa: bool

    creada_en: datetime


# =====================================================
# REGLAS
# =====================================================

class ReglaCreate(BaseModel):

    compania_id: UUID

    tipo_caso: str

    palabras_clave: List[str]

    prioridad: str

    siguiente_paso: str

    plantilla_justificacion: str


class ReglaResponse(BaseModel):

    id: UUID

    compania_id: UUID

    tipo_caso: str

    palabras_clave: List[str]

    prioridad: str

    siguiente_paso: str

    plantilla_justificacion: str

    creada_en: datetime


# =====================================================
# SOLICITUDES
# =====================================================

class SolicitudResponseAdmin(BaseModel):

    id: UUID

    compania_id: UUID

    solicitud_id: str

    estado: str

    id_caso_externo: Optional[str]

    creada_en: datetime


# =====================================================
# LOGS
# =====================================================

class LogResponse(BaseModel):

    id: UUID

    id_request: str

    compania_id: Optional[UUID]

    estado: str

    latencia_ms: Optional[int]

    codigo_error: Optional[str]

    creado_en: datetime
