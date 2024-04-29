"""Seed: Whisky

Revision ID: 37a885eb2639
Revises: 8a208be6362
Create Date: 2014-12-19 18:29:50.951595

"""

from csv import reader
from pathlib import Path

from alembic import op

from whiskyton.models import Whisky

# revision identifiers, used by Alembic.
revision = "37a885eb2639"
down_revision = "8a208be6362"


def upgrade():
    path = Path() / "migrations" / "csv" / "whisky.csv"
    with path.open() as file:
        lines = list(reader(file))
    headers = lines.pop(0)

    headers.append("slug")
    for line in lines:
        whisky = Whisky(distillery=line[0])
        line.append(whisky.get_slug())

    data = [dict(zip(headers, line)) for line in lines]

    op.bulk_insert(Whisky.__table__, data)


def downgrade():
    op.execute(Whisky.__table__.delete())
