"""Seed: page views by 2014-12-18

Revision ID: 544f5ee76f59
Revises: 447b2802474f
Create Date: 2014-12-19 18:34:24.364088

"""

# revision identifiers, used by Alembic.
revision = '544f5ee76f59'
down_revision = '447b2802474f'

from alembic import op
import sqlalchemy as sa

from csv import reader
from unipath import Path
from whiskyton import db
from whiskyton.models import Whisky


def upgrade():

    # main vars
    total_views = dict()
    file_handler = Path('migrations',
                        'csv',
                        '20140101-20141218_google_analytics.csv')

    # load csv data
    for path, views in reader(open(file_handler, 'r')):

        # get whisky id from database
        if '/w/' in path:
            whisky_id = int(path.replace('/w/', ''))
            whisky = Whisky.query.get(whisky_id)
        else:
            whisky_slug = path.replace('/', '')
            new_whisky = Whisky(distillery=whisky_slug)
            new_slug = new_whisky.get_slug()
            whisky = Whisky.query.filter(Whisky.slug == new_slug).first()

        # feed temporary dictionary
        if whisky is not None:
            total_views[whisky.id] = total_views.get(whisky.id, 0) + int(views)

    # update db
    for whisky_id in total_views.keys():
        new_whisky = Whisky.query.get(whisky_id)
        new_whisky.views = total_views[whisky_id]
        db.session.add(new_whisky)

    # commit
    db.session.commit()


def downgrade():
    whiskies = Whisky.query.all()
    for whisky in whiskies:
        whisky.views = 0
        db.session.add(whisky)
    db.session.commit()