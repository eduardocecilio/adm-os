"""add uuid to workspaces

Revision ID: f3a1b2c3d4e5
Revises: ddce44a43cf1
Create Date: 2026-03-18 10:37:00.000000

"""
from alembic import op
import sqlalchemy as sa
import uuid


# revision identifiers, used by Alembic.
revision = 'f3a1b2c3d4e5'
down_revision = 'ddce44a43cf1'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add column as nullable first
    op.add_column('workspaces', sa.Column('uuid', sa.String(), nullable=True))
    
    # 2. Populate existing rows with UUIDs
    # Get a connection to execute raw SQL
    conn = op.get_bind()
    workspaces = conn.execute(sa.text("SELECT id FROM workspaces")).fetchall()
    for ws in workspaces:
        conn.execute(
            sa.text("UPDATE workspaces SET uuid = :uuid WHERE id = :id"),
            {"uuid": str(uuid.uuid4()), "id": ws[0]}
        )
    
    # 3. Make non-nullable and add unique index
    op.alter_column('workspaces', 'uuid', nullable=False)
    op.create_index(op.f('ix_workspaces_uuid'), 'workspaces', ['uuid'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_workspaces_uuid'), table_name='workspaces')
    op.drop_column('workspaces', 'uuid')
