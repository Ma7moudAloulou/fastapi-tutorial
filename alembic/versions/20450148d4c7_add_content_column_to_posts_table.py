"""add content column to posts table

Revision ID: 20450148d4c7
Revises: 2e221f3afdbc
Create Date: 2023-09-22 23:36:00.444084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '20450148d4c7'
down_revision: Union[str, None] = '2e221f3afdbc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("content",sa.String(),nullable=False))


def downgrade() -> None:
    op.drop_column("posts","content")
    pass
