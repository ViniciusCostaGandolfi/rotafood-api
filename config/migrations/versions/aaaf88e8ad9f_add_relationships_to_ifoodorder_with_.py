"""add relationships to IFoodOrder with Order

Revision ID: aaaf88e8ad9f
Revises: cd4489c1837f
Create Date: 2024-01-15 16:48:53.107796

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aaaf88e8ad9f'
down_revision: Union[str, None] = 'cd4489c1837f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###
