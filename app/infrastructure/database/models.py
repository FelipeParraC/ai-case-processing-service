import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID

from app.infrastructure.database.base import Base


# =========================================================
# COMPANIAS
# =========================================================

class Compania(Base):

    __tablename__ = "companias"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nombre: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    creada_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    categorias = relationship(
        "Categoria",
        back_populates="compania",
        cascade="all, delete-orphan"
    )

    usa_servicio_prioridad_externo = Column(
        Boolean,
        default=False,
        nullable=False
    )

    activa: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

# =========================================================
# CATEGORIAS
# =========================================================

class Categoria(Base):

    __tablename__ = "categorias"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    compania_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companias.id"),
        nullable=False
    )

    nombre: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    descripcion: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    activa: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    creada_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    compania = relationship(
        "Compania",
        back_populates="categorias"
    )


# =========================================================
# REGLAS
# =========================================================

class Regla(Base):

    __tablename__ = "reglas"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    compania_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companias.id"),
        nullable=False
    )

    tipo_caso: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    palabras_clave: Mapped[list] = mapped_column(
        JSONB,
        nullable=False
    )

    prioridad: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    siguiente_paso: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    plantilla_justificacion: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    creada_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# LOGS DE SOLICITUDES
# =========================================================

class LogSolicitud(Base):

    __tablename__ = "logs_solicitudes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    id_request: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    compania_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companias.id"),
        nullable=True
    )

    estado: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    latencia_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    codigo_error: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    detalle_error: Mapped[dict] = mapped_column(
        JSONB,
        nullable=True
    )

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )


# =========================================================
# SOLICITUDES (CORE ENTITY)
# =========================================================

class Solicitud(Base):

    __tablename__ = "solicitudes"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    compania_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companias.id"),
        nullable=False
    )

    solicitud_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    id_request: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    estado: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    id_caso_externo: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    respuesta_json: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    creada_en: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "compania_id",
            "solicitud_id",
            name="uq_compania_solicitud"
        ),
    )
