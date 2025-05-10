"""create_security_tables

Revision ID: af2d354d48a2
Revises:
Create Date: 2025-05-08 13:52:05.793067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import func


# revision identifiers, used by Alembic.
revision: str = 'af2d354d48a2'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def common_columns():
    return [
        sa.Column('version', sa.Integer, server_default=sa.text('1'), nullable=False),
        sa.Column('create_ts', sa.TIMESTAMP(timezone=True), server_default=func.now()),
        sa.Column('created_by', sa.String(50)),
        sa.Column('update_ts', sa.TIMESTAMP(timezone=True), onupdate=func.now()),
        sa.Column('updated_by', sa.String(50)),
        sa.Column('delete_ts', sa.TIMESTAMP(timezone=True)),
        sa.Column('deleted_by', sa.String(50)),
    ]


def upgrade() -> None:
    """Upgrade schema."""
    op.execute('CREATE EXTENSION IF NOT EXISTS pgcrypto')
    op.create_table(
        'sec_role',
        sa.Column('id',
            sa.dialects.postgresql.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            primary_key=True,
            nullable=False
        ),
        *common_columns(),
        sa.Column('name', sa.String(length=50), nullable=False),
    )

    op.create_table(
        'sec_user',
        sa.Column('id',
            sa.dialects.postgresql.UUID(),
            server_default=sa.text('gen_random_uuid()'),
            primary_key=True,
            nullable=False
        ),
        *common_columns(),
        sa.Column('username', sa.String(length=50), nullable=False),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('phone', sa.String(length=20), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('role_id', sa.dialects.postgresql.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['sec_role.id']),
    )

    op.execute("""
        INSERT INTO sec_role (name) VALUES
        ('FULL_ACCESS'),
        ('INTEGRATION_ROLE')
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('sec_user')
    op.drop_table('sec_role')
