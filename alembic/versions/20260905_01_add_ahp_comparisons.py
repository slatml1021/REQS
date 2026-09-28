"""Add persistent AHP pairwise comparisons.

Revision ID: 20260905_01
Revises: 20260903_01
Create Date: 2026-09-05
"""

from alembic import op
import sqlalchemy as sa


revision = "20260905_01"
down_revision = "20260903_01"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ahp_comparisons",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("requirement_a_id", sa.Integer(), nullable=False),
        sa.Column("requirement_b_id", sa.Integer(), nullable=False),
        sa.Column("comparison_value", sa.Numeric(10, 8), nullable=False),
        sa.CheckConstraint("requirement_a_id < requirement_b_id", name="ck_ahp_canonical_pair"),
        sa.CheckConstraint("comparison_value > 0 AND comparison_value <= 9", name="ck_ahp_value_range"),
        sa.ForeignKeyConstraint(["requirement_a_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["requirement_b_id"], ["requirements.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("requirement_a_id", "requirement_b_id", name="uq_ahp_pair"),
    )
    op.create_index("ix_ahp_comparisons_requirement_a_id", "ahp_comparisons", ["requirement_a_id"])
    op.create_index("ix_ahp_comparisons_requirement_b_id", "ahp_comparisons", ["requirement_b_id"])


def downgrade() -> None:
    op.drop_index("ix_ahp_comparisons_requirement_b_id", table_name="ahp_comparisons")
    op.drop_index("ix_ahp_comparisons_requirement_a_id", table_name="ahp_comparisons")
    op.drop_table("ahp_comparisons")
