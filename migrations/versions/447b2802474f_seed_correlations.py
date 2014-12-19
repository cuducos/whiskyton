"""Seed: Correlations

Revision ID: 447b2802474f
Revises: 37a885eb2639
Create Date: 2014-12-19 18:32:11.305999

"""

# revision identifiers, used by Alembic.
revision = '447b2802474f'
down_revision = '37a885eb2639'

from alembic import op
import sqlalchemy as sa

from whiskyton import db
from whiskyton.models import Whisky, Correlation


def upgrade():

    # create basic vars
    whiskies = Whisky.query.all()
    correlations = list()
    data = list()

    # loop twice to compare all whiskies
    for reference in whiskies:
        for whisky in whiskies:

            # add correlation if it does not already exists
            item = (whisky.id, reference.id)
            if item not in correlations and whisky.id != reference.id:
                data.append(reference.get_correlation(whisky))
                correlations.append(item)

    # bulk insert
    op.bulk_insert(Correlation.__table__, data)


def downgrade():
    op.execute(Correlation.__table__.delete())

