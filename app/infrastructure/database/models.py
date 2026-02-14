import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from app.infrastructure.database.base import Base

class Company(Base):

    __tablename__ = "companies"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    nombre = Column(
        String,
        unique=True,
        nullable=False
    )

    categories = relationship(
        "Category",
        back_populates="company",
        cascade="all, delete-orphan"
    )



class Category(Base):

    __tablename__ = "categories"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    description: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    company = relationship("Company", back_populates="categories")


class Rule(Base):

    __tablename__ = "rules"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    compania_id = Column(
        UUID(as_uuid=True),
        ForeignKey("companies.id"),
        nullable=False
    )

    case_type = Column(String)

    keywords = Column(JSONB)

    priority = Column(String)

    next_step = Column(String)

    justification_template = Column(String)


class RequestLog(Base):

    __tablename__ = "requests_log"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    request_id: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    latency_ms: Mapped[int] = mapped_column(
        Integer,
        nullable=True
    )

    error_code: Mapped[str] = mapped_column(
        String,
        nullable=True
    )

    error_detail: Mapped[dict] = mapped_column(
        JSON,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

class SolicitudRecord(Base):

    __tablename__ = "solicitudes"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )

    solicitud_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    request_id: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    external_case_id: Mapped[str | None] = mapped_column(
        String,
        nullable=True
    )

    response_json: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "solicitud_id",
            name="uq_company_solicitud"
        ),
    )