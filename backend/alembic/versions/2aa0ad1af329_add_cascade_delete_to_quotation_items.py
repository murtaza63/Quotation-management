"""add cascade delete to quotation items

Revision ID: 2aa0ad1af329
Revises: a5191d86f760
Create Date: 2026-08-27 12:29:40.096832
"""

from typing import Sequence, Union

from alembic import op

revision: str = "2aa0ad1af329"
down_revision: Union[str, Sequence[str], None] = "a5191d86f760"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_constraint(
        "quotation_items_quotation_id_fkey",
        "quotation_items",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "quotation_items_quotation_id_fkey",
        "quotation_items",
        "quotations",
        ["quotation_id"],
        ["id"],
        ondelete="CASCADE",
    )


def downgrade() -> None:
    op.drop_constraint(
        "quotation_items_quotation_id_fkey",
        "quotation_items",
        type_="foreignkey",
    )

    op.create_foreign_key(
        "quotation_items_quotation_id_fkey",
        "quotation_items",
        "quotations",
        ["quotation_id"],
        ["id"],
    )
