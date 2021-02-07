"""create todo table

Revision ID: dda65a1d96bb
Revises: 
Create Date: 2021-01-31 00:03:19.637215

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "dda65a1d96bb"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "todo",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("todo")
