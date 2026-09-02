"""Persisted calculation inputs and results for all prioritization methods."""

from enum import StrEnum

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, JSON, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class PriorityMethod(StrEnum):
    AHP = "ahp"
    WIEGERS = "wiegers"
    VOLERE = "volere"


class PriorityScore(Base):
    __tablename__ = "priority_scores"
    __table_args__ = (
        CheckConstraint("raw_score >= 0", name="ck_priority_raw_score_nonnegative"),
        CheckConstraint("normalized_score >= 0 AND normalized_score <= 100", name="ck_priority_normalized_score_range"),
        UniqueConstraint("requirement_id", "method", name="uq_requirement_priority_method"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    requirement_id: Mapped[int] = mapped_column(ForeignKey("requirements.id", ondelete="CASCADE"), index=True)
    method: Mapped[PriorityMethod] = mapped_column(Enum(PriorityMethod, name="priority_method"))
    raw_score: Mapped[float] = mapped_column(Numeric(12, 4))
    normalized_score: Mapped[float] = mapped_column(Numeric(5, 2))
    inputs: Mapped[dict] = mapped_column(JSON, default=dict)

    requirement: Mapped["Requirement"] = relationship(back_populates="priority_scores")
