"""Change user id type to bigint

Revision ID: eacede064922
Revises: 00b4a4a580fc
Create Date: 2024-11-01 00:59:36.529125

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "eacede064922"
down_revision: Union[str, None] = "00b4a4a580fc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "id",
        existing_type=sa.INTEGER(),
        type_=sa.BIGINT(),
        existing_nullable=False,
        autoincrement=True,
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "users",
        "id",
        existing_type=sa.BIGINT(),
        type_=sa.INTEGER(),
        existing_nullable=False,
        autoincrement=True,
    )
    # ### end Alembic commands ###