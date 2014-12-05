# coding: utf-8

"""Seed whiskies

Revision ID: 1ce5878c9d7f
Revises: 17f96fb856ef
Create Date: 2014-08-28 13:08:02.243929

"""

# revision identifiers, used by Alembic.

revision = '1ce5878c9d7f'
down_revision = '17f96fb856ef'

import csv
from alembic import op
from unipath import Path
from whiskyton.models import Whisky


def upgrade():

    file_name = Path('migrations', 'csv', 'whisky.csv')
    reader = csv.reader(open(file_name, 'r'))

    lines = list(reader)
    headers = lines.pop(0)

    headers.append('slug')
    for line in lines:
        whisky = Whisky(distillery=line[0])
        line.append(whisky.get_slug())

    data = [dict(zip(headers, line)) for line in lines]

    op.bulk_insert(Whisky.__table__, data)


def downgrade():
    op.execute(Whisky.__table__.delete())