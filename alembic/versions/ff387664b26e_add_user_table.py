"""add user table

Revision ID: ff387664b26e
Revises: 20450148d4c7
Create Date: 2023-09-22 23:46:41.137965

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff387664b26e'
down_revision: Union[str, None] = '20450148d4c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users",
                    sa.Column("id",sa.Integer(),nullable=False),
                    sa.Column("email", sa.String(), nullable=False),
                    sa.Column("password", sa.String(), nullable=False),
                    sa.Column("created_at", sa.TIMESTAMP(timezone=True), server_default=sa.text("now()"), nullable=False),
                    sa.PrimaryKeyConstraint("id"),
                    sa.UniqueConstraint("email")                   
    )
    
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
