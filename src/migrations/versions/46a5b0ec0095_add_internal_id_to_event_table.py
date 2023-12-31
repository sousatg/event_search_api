"""Add internal id to event table

Revision ID: 46a5b0ec0095
Revises: a42d4e128bb7
Create Date: 2023-08-15 23:43:18.517300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "46a5b0ec0095"
down_revision = "a42d4e128bb7"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.add_column(sa.Column("internal_id", sa.String(), nullable=True))
        batch_op.create_index(
            batch_op.f("ix_events_internal_id"), ["internal_id"], unique=True
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("events", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_events_internal_id"))
        batch_op.drop_column("internal_id")

    # ### end Alembic commands ###
