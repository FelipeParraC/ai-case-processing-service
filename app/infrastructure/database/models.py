import uuid
from datetime import datetime

from sqlalchemy import (
    String,
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    JSON,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.database.session import Base


class Company(Base):

    __tablename__ = "companies"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String, nullable=False)

    code: Mapped[str] = mapped_column(
        String,
        unique=True,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    categories = relationship("Category", back_populates="company")


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

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4
    )

    company_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("companies.id"),
        nullable=False
    )

    rule_type: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    config: Mapped[dict] = mapped_column(
        JSON,
        nullable=False
    )

    version: Mapped[int] = mapped_column(
        Integer,
        default=1
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )


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
