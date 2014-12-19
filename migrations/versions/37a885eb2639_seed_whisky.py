"""Seed: Whisky

Revision ID: 37a885eb2639
Revises: 8a208be6362
Create Date: 2014-12-19 18:29:50.951595

"""

# revision identifiers, used by Alembic.
revision = '37a885eb2639'
down_revision = '8a208be6362'

from alembic import op
import sqlalchemy as sa

from csv import reader
from unipath import Path
from whiskyton.models import Whisky


def upgrade():

    file_name = Path('migrations', 'csv', 'whisky.csv')
    lines = list(reader(open(file_name, 'r')))
    headers = lines.pop(0)

    headers.append('slug')
    for line in lines:
        whisky = Whisky(distillery=line[0])
        line.append(whisky.get_slug())

    data = [dict(zip(headers, line)) for line in lines]

    op.bulk_insert(Whisky.__table__, data)


def downgrade():
    op.execute(Whisky.__table__.delete())

