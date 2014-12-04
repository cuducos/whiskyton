# coding: utf-8

import unittest
from whiskyton import app, db
from whiskyton.models import Whisky, Correlation
from whiskyton.helpers import whisky, charts


class TestRoutes(unittest.TestCase):

    def setUp(self):

        # test db settings
        db_uri = 'sqlite:///' + app.config['BASEDIR'].child('tests.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

        # init
        app.testing = True
        self.app = app.test_client()
        db.create_all()

        # feed db: whiskies
        whisky_1 = Whisky(
            distillery='Bowmore',
            body=2,
            sweetness=2,
            smoky=3,
            medicinal=1,
            tobacco=0,
            honey=2,
            spicy=2,
            winey=1,
            nutty=1,
            malty=1,
            fruity=1,
            floral=2,
            postcode='PA43 7GS',
            latitude=131330,
            longitude=659720,
            slug='bowmore'
        )
        whisky_2 = Whisky(
            distillery='Glen Deveron / MacDuff',
            body=2,
            sweetness=3,
            smoky=1,
            medicinal=1,
            tobacco=1,
            honey=1,
            spicy=1,
            winey=2,
            nutty=0,
            malty=2,
            fruity=0,
            floral=1,
            postcode='AB4 3JT',
            latitude=372120,
            longitude=860400,
            slug='glendeveronmacduff'
        )
        db.session.add(whisky_1)
        db.session.add(whisky_2)
        db.session.commit()

        # feed db: correlations
        self.whisky_1 = Whisky.query.get(1)
        self.whisky_2 = Whisky.query.get(2)
        row_1 = whisky.get_correlation(self.whisky_1, self.whisky_2)
        row_2 = whisky.get_correlation(self.whisky_2, self.whisky_1)
        db.session.add(Correlation(**row_1))
        db.session.add(Correlation(**row_2))

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # test routes from whiskyton/blueprint/site.py

    def test_index(self):
        resp = self.app.get('/')
        assert resp.status_code == 200

    def test_search(self):
        resp_1 = self.app.get('/search?s={}'.format(self.whisky_1.distillery))
        resp_2 = self.app.get('/search?s=Bowm')
        assert resp_1.status_code == 302
        assert resp_2.status_code == 200

    def test_whisky_page(self):
        resp_1 = self.app.get('/{}'.format(self.whisky_1.slug))
        resp_2 = self.app.get('/{}'.format(self.whisky_2.slug))
        resp_3 = self.app.get('/jackdaniels')
        assert resp_1.status_code == 200
        assert resp_2.status_code == 200
        assert resp_3.status_code == 404

    def test_search_id(self):
        resp_1 = self.app.get('/w/{}'.format(self.whisky_1.id))
        resp_2 = self.app.get('/w/{}'.format(6.02e+23))
        assert resp_1.status_code == 302
        assert resp_2.status_code == 404

    # test routes from whiskyton/blueprints/files.py

    def test_create_chart(self):
        tastes_1 = whisky.get_tastes(self.whisky_1)
        tastes_2 = whisky.get_tastes(self.whisky_2)
        cache_name = charts.cache_name(tastes_1, tastes_2, True)
        if cache_name.exists():
            cache_name.remove()
        svg_1 = '{}-{}.svg'.format(self.whisky_1.slug, self.whisky_2.slug)
        svg_2 = 'jackdaniels-jameson.svg'
        resp_1 = self.app.get('/charts/{}'.format(svg_1))
        resp_2 = self.app.get('/charts/{}'.format(svg_2))
        assert resp_1.status_code == 200
        assert resp_2.status_code == 404

    def test_bootstrap_fonts(self):
        base_url = '/static/fonts/glyphicons-halflings-regular.'
        extensions = ['eot', 'svg', 'ttf', 'woff', 'py']
        for ext in extensions:
            resp = self.app.get(base_url + ext)
            if ext is not 'py':
                assert resp.status_code == 200
            else:
                assert resp.status_code == 404

    def test_whisky_json(self):
        resp = self.app.get('/whiskyton.json')
        assert resp.status_code == 200

    def test_robots(self):
        resp = self.app.get('/robots.txt')
        assert resp.status_code in [200, 304]

    def test_favicon(self):
        resp = self.app.get('/favicon.ico')
        assert resp.status_code in [200, 304]

    def test_sitemap(self):
        resp = self.app.get('/sitemap.xml')
        assert resp.status_code == 200
