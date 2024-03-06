"""change penerbit to publisher

Revision ID: 1ae0014b536e
Revises: 152b69bd5207
Create Date: 2024-03-05 22:12:47.639562

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1ae0014b536e'
down_revision = '152b69bd5207'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('publisher', sa.String(length=80), nullable=True))
        batch_op.drop_column('penerbit')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('book', schema=None) as batch_op:
        batch_op.add_column(sa.Column('penerbit', sa.VARCHAR(length=60), autoincrement=False, nullable=True))
        batch_op.drop_column('publisher')

    # ### end Alembic commands ###
