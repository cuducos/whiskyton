"""Seed whiskies

Revision ID: 1ce5878c9d7f
Revises: 17f96fb856ef
Create Date: 2014-08-28 13:08:02.243929

"""

# revision identifiers, used by Alembic.
import csv
from unipath import Path
from whiskyton.whisky import slugfy

revision = '1ce5878c9d7f'
down_revision = '17f96fb856ef'

from alembic import op
import sqlalchemy as sa

from whiskyton.models import Whisky

def upgrade():
    fname = Path('migrations', 'csv', 'whisky.csv')
    reader = csv.reader(open(fname, 'r'))

    lines = list(reader)
    headers = lines.pop(0)

    headers.append('slug')
    for line in lines:
        line.append(slugfy(line[0]))

    data = [dict(zip(headers, line)) for line in lines]

    op.bulk_insert(Whisky.__table__, data)


def downgrade():
    op.execute(Whisky.__table__.delete())
