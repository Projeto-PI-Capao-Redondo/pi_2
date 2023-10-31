"""ajuste

Revision ID: 91db0833c3ad
Revises: de47d70e656e
Create Date: 2023-10-31 14:56:14.127392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '91db0833c3ad'
down_revision: Union[str, None] = 'de47d70e656e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('loja', 'complemento',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('loja', 'complemento',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###