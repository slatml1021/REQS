"""Directed traceability relations between requirements."""

from enum import StrEnum

from sqlalchemy import CheckConstraint, Enum, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class RelationType(StrEnum):
    DEPENDS_ON = "depends_on"
    PREREQUISITE_OF = "prerequisite_of"
    REFINES = "refines"
    RELATED_TO = "related_to"


class RequirementRelation(Base):
    __tablename__ = "requirement_relations"
    __table_args__ = (
        CheckConstraint("source_requirement_id <> target_requirement_id", name="ck_relation_no_self_reference"),
        UniqueConstraint("source_requirement_id", "target_requirement_id", "relation_type", name="uq_relation"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    source_requirement_id: Mapped[int] = mapped_column(ForeignKey("requirements.id", ondelete="CASCADE"), index=True)
    target_requirement_id: Mapped[int] = mapped_column(ForeignKey("requirements.id", ondelete="CASCADE"), index=True)
    relation_type: Mapped[RelationType] = mapped_column(Enum(RelationType, name="relation_type"))

    source: Mapped["Requirement"] = relationship(back_populates="outgoing_relations", foreign_keys=[source_requirement_id])
    target: Mapped["Requirement"] = relationship(back_populates="incoming_relations", foreign_keys=[target_requirement_id])
