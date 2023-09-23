"""add last few columns to posts table

Revision ID: d0a47b57c038
Revises: bec4aae28c79
Create Date: 2023-09-23 00:21:11.173787

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd0a47b57c038'
down_revision: Union[str, None] = 'bec4aae28c79'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts",sa.Column("published", sa.Boolean(), nullable=False, server_default="TRUE"),)

    op.add_column("posts",sa.Column("created_at",sa.TIMESTAMP(timezone=True),nullable=False, server_default=sa.text("NOW()")),)
    
    pass


def downgrade() -> None:
    op.drop_column("posts","published")
    op.drop_column("posts","created_at")
    pass
