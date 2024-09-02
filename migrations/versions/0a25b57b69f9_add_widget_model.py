"""add widget model

Revision ID: 0a25b57b69f9
Revises: 23d27124d382
Create Date: 2024-07-29 14:30:28.849205

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '0a25b57b69f9'
down_revision: Union[str, None] = '23d27124d382'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('widget',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('account', sa.UUID(), nullable=False),
    sa.Column('data', sa.UUID(), nullable=False),
    sa.Column('settings', sa.JSON(), nullable=False),
    sa.Column('time_create', sa.DateTime(timezone=True), nullable=True),
    sa.Column('time_update', sa.DateTime(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['account'], ['account.id'], ),
    sa.ForeignKeyConstraint(['data'], ['data.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('widget')
    # ### end Alembic commands ###
