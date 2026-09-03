"""Create the initial REQS persistence schema.

Revision ID: 20260903_01
Revises:
Create Date: 2026-09-03
"""

from alembic import op
import sqlalchemy as sa


revision = "20260903_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    relation_type = sa.Enum("DEPENDS_ON", "PREREQUISITE_OF", "REFINES", "RELATED_TO", name="relation_type")
    priority_method = sa.Enum("AHP", "WIEGERS", "VOLERE", name="priority_method")
    bind = op.get_bind()
    relation_type.create(bind, checkfirst=True)
    priority_method.create(bind, checkfirst=True)
    op.create_table(
        "requirements",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("key", sa.String(length=32), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("key"),
    )
    op.create_index("ix_requirements_key", "requirements", ["key"])
    op.create_table(
        "requirement_relations",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("source_requirement_id", sa.Integer(), nullable=False),
        sa.Column("target_requirement_id", sa.Integer(), nullable=False),
        sa.Column("relation_type", relation_type, nullable=False),
        sa.CheckConstraint("source_requirement_id <> target_requirement_id", name="ck_relation_no_self_reference"),
        sa.ForeignKeyConstraint(["source_requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["target_requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("source_requirement_id", "target_requirement_id", "relation_type", name="uq_relation"),
    )
    op.create_index("ix_requirement_relations_source_requirement_id", "requirement_relations", ["source_requirement_id"])
    op.create_index("ix_requirement_relations_target_requirement_id", "requirement_relations", ["target_requirement_id"])
    op.create_table(
        "priority_scores",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("requirement_id", sa.Integer(), nullable=False),
        sa.Column("method", priority_method, nullable=False),
        sa.Column("raw_score", sa.Numeric(12, 4), nullable=False),
        sa.Column("normalized_score", sa.Numeric(5, 2), nullable=False),
        sa.Column("inputs", sa.JSON(), nullable=False),
        sa.CheckConstraint("raw_score >= 0", name="ck_priority_raw_score_nonnegative"),
        sa.CheckConstraint("normalized_score >= 0 AND normalized_score <= 100", name="ck_priority_normalized_score_range"),
        sa.ForeignKeyConstraint(["requirement_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("requirement_id", "method", name="uq_requirement_priority_method"),
    )
    op.create_index("ix_priority_scores_requirement_id", "priority_scores", ["requirement_id"])


def downgrade() -> None:
    op.drop_index("ix_priority_scores_requirement_id", table_name="priority_scores")
    op.drop_table("priority_scores")
    op.drop_index("ix_requirement_relations_target_requirement_id", table_name="requirement_relations")
    op.drop_index("ix_requirement_relations_source_requirement_id", table_name="requirement_relations")
    op.drop_table("requirement_relations")
    op.drop_index("ix_requirements_key", table_name="requirements")
    op.drop_table("requirements")
    bind = op.get_bind()
    sa.Enum(name="priority_method").drop(bind, checkfirst=True)
    sa.Enum(name="relation_type").drop(bind, checkfirst=True)
