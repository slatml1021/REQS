"""Requirement entity and lifecycle status."""

from datetime import datetime

from sqlalchemy import DateTime, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Requirement(Base):
    __tablename__ = "requirements"

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(32), default="draft")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    outgoing_relations: Mapped[list["RequirementRelation"]] = relationship(
        back_populates="source", foreign_keys="RequirementRelation.source_requirement_id", cascade="all, delete-orphan"
    )
    incoming_relations: Mapped[list["RequirementRelation"]] = relationship(
        back_populates="target", foreign_keys="RequirementRelation.target_requirement_id", cascade="all, delete-orphan"
    )
    priority_scores: Mapped[list["PriorityScore"]] = relationship(
        back_populates="requirement", cascade="all, delete-orphan"
    )
