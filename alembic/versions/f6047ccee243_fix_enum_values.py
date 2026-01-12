"""fix enum values

Revision ID: f6047ccee243
Revises: 61061895e90b
Create Date: 2026-01-12 16:57:19.027530

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = 'f6047ccee243'
down_revision: Union[str, Sequence[str], None] = '61061895e90b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    notification_status_enum = postgresql.ENUM(
        'PENDING',
        'SENT',
        'FAILED',
        name='notificationstatus'
    )

    # 1️⃣ создать enum
    notification_status_enum.create(op.get_bind(), checkfirst=True)

    # 2️⃣ добавить колонку С DEFAULT
    op.add_column(
        'notifications',
        sa.Column(
            'status',
            notification_status_enum,
            nullable=False,
            server_default='PENDING'
        )
    )

    # 3️⃣ убрать default (чтобы ORM управлял статусом)
    op.alter_column(
        'notifications',
        'status',
        server_default=None
    )


def downgrade():
    op.drop_column('notifications', 'status')

    notification_status_enum = postgresql.ENUM(
        'PENDING',
        'SENT',
        'FAILED',
        name='notificationstatus'
    )
    notification_status_enum.drop(op.get_bind(), checkfirst=True)
