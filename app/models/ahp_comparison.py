"""Stored pairwise judgments used by the AHP prioritization module."""

from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class AhpComparison(Base):
    """A canonical AHP ratio between two distinct requirements.

    Requirement IDs are stored in ascending order. ``comparison_value`` therefore
    always expresses the importance of ``requirement_a`` relative to
    ``requirement_b`` and prevents duplicate inverse pairs.
    """

    __tablename__ = "ahp_comparisons"
    __table_args__ = (
        CheckConstraint("requirement_a_id < requirement_b_id", name="ck_ahp_canonical_pair"),
        CheckConstraint("comparison_value > 0 AND comparison_value <= 9", name="ck_ahp_value_range"),
        UniqueConstraint("requirement_a_id", "requirement_b_id", name="uq_ahp_pair"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    requirement_a_id: Mapped[int] = mapped_column(ForeignKey("requirements.id", ondelete="CASCADE"), index=True)
    requirement_b_id: Mapped[int] = mapped_column(ForeignKey("requirements.id", ondelete="CASCADE"), index=True)
    comparison_value: Mapped[Decimal] = mapped_column(Numeric(10, 8))
