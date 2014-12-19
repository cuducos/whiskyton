# coding: utf-8

"""Seed correlations

Revision ID: 4cbf0230c35
Revises: 1ce5878c9d7f
Create Date: 2014-09-02 07:42:34.270581

"""

# revision identifiers, used by Alembic.
revision = '4cbf0230c35'
down_revision = '1ce5878c9d7f'

from alembic import op
from whiskyton import app, db
from whiskyton.models import Whisky, Correlation


def upgrade():

    # create basic vars
    whiskies = db.session.query(Whisky.id,
                                Whisky.body,
                                Whisky.sweetness,
                                Whisky.smoky,
                                Whisky.medicinal,
                                Whisky.tobacco,
                                Whisky.honey,
                                Whisky.spicy,
                                Whisky.winey,
                                Whisky.nutty,
                                Whisky.malty,
                                Whisky.fruity,
                                Whisky.floral).all()
    correlations = list()
    data = list()

    # loop twice to compare all whiskies
    for reference in whiskies:
        for whisky in whiskies:

            # add correlation if it does not already exists
            item = (whisky.id, reference.id)
            if item not in correlations and whisky.id != reference.id:
                whisky_obj = Whisky(id=whisky.id,
                                    body=whisky.body,
                                    sweetness=whisky.sweetness,
                                    smoky=whisky.smoky,
                                    medicinal=whisky.medicinal,
                                    tobacco=whisky.tobacco,
                                    honey=whisky.honey,
                                    spicy=whisky.spicy,
                                    winey=whisky.winey,
                                    nutty=whisky.nutty,
                                    malty=whisky.malty,
                                    fruity=whisky.fruity,
                                    floral=whisky.floral)
                reference_obj = Whisky(id=reference.id,
                                       body=reference.body,
                                       sweetness=reference.sweetness,
                                       smoky=reference.smoky,
                                       medicinal=reference.medicinal,
                                       tobacco=reference.tobacco,
                                       honey=reference.honey,
                                       spicy=reference.spicy,
                                       winey=reference.winey,
                                       nutty=reference.nutty,
                                       malty=reference.malty,
                                       fruity=reference.fruity,
                                       floral=reference.floral)
                data.append(reference_obj.get_correlation(whisky_obj))
                correlations.append(item)

    # bulk insert
    op.bulk_insert(Correlation.__table__, data)


def downgrade():
    op.execute(Correlation.__table__.delete())
