"""add_reminder_to_notification_type

Revision ID: eee66731e00e
Revises: 8d3b4b461dc8
Create Date: 2026-04-10 21:37:13.628140

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'eee66731e00e'
down_revision = '8d3b4b461dc8'
branch_labels = None
depends_on = None


def upgrade():
    op.execute(
        "ALTER TABLE notification MODIFY COLUMN type ENUM('SYSTEM', 'APPOINTMENT', 'PROMOTION', 'REMINDER')"
    )

def downgrade():
    op.execute(
        "ALTER TABLE notification MODIFY COLUMN type ENUM('SYSTEM', 'APPOINTMENT', 'PROMOTION')"
    )