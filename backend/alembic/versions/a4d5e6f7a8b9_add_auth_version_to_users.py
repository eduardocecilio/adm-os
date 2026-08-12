"""add auth version to users

Revision ID: a4d5e6f7a8b9
Revises: f3a1b2c3d4e5
Create Date: 2026-08-12 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = "a4d5e6f7a8b9"
down_revision = "f3a1b2c3d4e5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column("auth_version", sa.Integer(), nullable=False, server_default="0"),
    )


def downgrade() -> None:
    op.drop_column("users", "auth_version")
