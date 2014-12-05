# coding: utf-8

"""seed_correlations

Revision ID: 4cbf0230c35
Revises: 1ce5878c9d7f
Create Date: 2014-09-02 07:42:34.270581

"""

# revision identifiers, used by Alembic.
revision = '4cbf0230c35'
down_revision = '1ce5878c9d7f'

from alembic import op
from whiskyton import app
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
