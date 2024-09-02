"""add title on data model

Revision ID: 9f1c54b22dad
Revises: 79e60263c381
Create Date: 2024-07-24 14:35:48.940077

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '9f1c54b22dad'
down_revision: Union[str, None] = '79e60263c381'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('data', sa.Column('title', sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('data', 'title')
    # ### end Alembic commands ###
