"""alter ids to autoincrement 

Revision ID: 4527d1c0a23d
Revises: 424b293cf56a
Create Date: 2023-12-13 09:57:50.877180

"""
from typing import Sequence, Union

from migrations import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4527d1c0a23d'
down_revision: Union[str, None] = '424b293cf56a'
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