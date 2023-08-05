"""create_figures_table

Revision ID: f1ada2484fe2
Revises: 04ae19b32c08
Create Date: 2022-03-17 15:57:28.225697+00:00

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
from sqlalchemy.engine import Inspector

revision = "f1ada2484fe2"
down_revision = "04ae19b32c08"
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    inspector = Inspector.from_engine(conn)
    tables = inspector.get_table_names()
    # ### commands auto generated by Alembic - please adjust! ###
    if "Figures" not in tables:
        op.create_table(
            "Figures",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("experiment_id", sa.Integer(), nullable=False),
            sa.Column("figure", sa.String(), nullable=False),
            sa.Column("time", sa.DATETIME(), nullable=False),
            sa.ForeignKeyConstraint(
                ["experiment_id"], ["Experiments.id"], ondelete="CASCADE"
            ),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade():
    op.drop_table("Figures")
