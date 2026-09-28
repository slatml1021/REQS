"""Add indexes for REQS priority and traceability query paths.

Revision ID: 20260928_02
Revises: 20260905_01
Create Date: 2026-09-28
"""

from alembic import op


revision = "20260928_02"
down_revision = "20260905_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_index("ix_priority_scores_method_normalized", "priority_scores", ["method", "normalized_score"])
    op.create_index("ix_requirement_relations_source_target", "requirement_relations", ["source_requirement_id", "target_requirement_id"])
    op.create_index("ix_requirement_relations_target_source", "requirement_relations", ["target_requirement_id", "source_requirement_id"])


def downgrade() -> None:
    op.drop_index("ix_requirement_relations_target_source", table_name="requirement_relations")
    op.drop_index("ix_requirement_relations_source_target", table_name="requirement_relations")
    op.drop_index("ix_priority_scores_method_normalized", table_name="priority_scores")
