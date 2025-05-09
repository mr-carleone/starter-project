"""add_to_field_sec_user

Revision ID: 2f6aa9ef82c0
Revises: af2d354d48a2
Create Date: 2025-05-10 00:41:22.660131

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f6aa9ef82c0'
down_revision: Union[str, None] = 'af2d354d48a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Добавляем новое поле is_active с default=False
    op.add_column('sec_user',
        sa.Column('is_active',
            sa.Boolean(),
            server_default=sa.text('false'),  # Дефолтное значение на уровне БД
            nullable=False,                    # Обязательное поле
            comment='Активен ли пользователь'
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Удаляем поле при откате миграции
    op.drop_column('sec_user', 'is_active')
