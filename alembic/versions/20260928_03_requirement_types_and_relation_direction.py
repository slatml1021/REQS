"""Add requirement types and full relation semantics.

Revision ID: 20260928_03
Revises: 20260928_02
Create Date: 2026-09-28
"""

from alembic import op
import sqlalchemy as sa


revision = "20260928_03"
down_revision = "20260928_02"
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    if bind.dialect.name == "postgresql":
        op.execute("ALTER TYPE relation_type ADD VALUE IF NOT EXISTS 'SIMILAR_TO'")
        op.execute("ALTER TYPE relation_type ADD VALUE IF NOT EXISTS 'CONFLICTS_WITH'")
    op.add_column(
        "requirements",
        sa.Column("requirement_type", sa.String(length=32), nullable=False, server_default="functional"),
    )
    op.add_column(
        "requirement_relations",
        sa.Column("is_directional", sa.Boolean(), nullable=False, server_default=sa.true()),
    )


def downgrade() -> None:
    op.drop_column("requirement_relations", "is_directional")
    op.drop_column("requirements", "requirement_type")
    # PostgreSQL enum values cannot be safely removed in place.
