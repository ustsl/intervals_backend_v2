"""userlist false

Revision ID: a50975db2a1d
Revises: 54625854f192
Create Date: 2024-07-22 16:46:08.137803

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a50975db2a1d'
down_revision: Union[str, None] = '54625854f192'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'account', ['user'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'account', type_='unique')
    # ### end Alembic commands ###
