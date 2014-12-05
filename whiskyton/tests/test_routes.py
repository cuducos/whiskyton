# coding: utf-8
import tempfile
import unittest
from whiskyton import app, db
from whiskyton.models import Whisky, Correlation
from whiskyton.helpers.charts import Chart


class TestRoutes(unittest.TestCase):

    def setUp(self):

        # test db settings
        db_uri = 'sqlite:///' + tempfile.mkstemp()[1]
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri

        # init
        app.testing = True
        self.app = app.test_client()
        db.create_all()

        # feed db: whiskies
        self.whisky_1 = Whisky(
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
        self.whisky_2 = Whisky(
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
        correlation_1 = self.whisky_1.get_correlation(self.whisky_2)
        correlation_2 = self.whisky_2.get_correlation(self.whisky_1)
        self.correlation_1 = Correlation(**correlation_1)
        self.correlation_2 = Correlation(**correlation_2)

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    # test routes from whiskyton/blueprint/site.py

    def test_index(self):
        db.session.add(self.whisky_1)
        db.session.commit()
        resp = self.app.get('/')
        assert resp.status_code == 200

    def test_search(self):
        db.session.add(self.whisky_1)
        db.session.commit()
        resp_1 = self.app.get('/search?s={}'.format(self.whisky_1.distillery))
        resp_2 = self.app.get('/search?s=Bowm')
        assert resp_1.status_code == 302
        assert resp_2.status_code == 200

    def test_whisky_page(self):
        db.session.add(self.whisky_1)
        db.session.add(self.whisky_2)
        db.session.add(self.correlation_1)
        db.session.add(self.correlation_2)
        db.session.commit()
        for row in Whisky.query.all():
            resp = self.app.get('/{}'.format(row.slug))
            assert resp.status_code == 200
        fake = self.app.get('/jackdaniels')
        assert fake.status_code == 404

    def test_search_id(self):
        db.session.add(self.whisky_1)
        db.session.commit()
        row = Whisky.query.first()
        resp_1 = self.app.get('/w/{}'.format(row.id))
        resp_2 = self.app.get('/w/{}'.format(6.02e+23))
        assert resp_1.status_code == 302
        assert resp_2.status_code == 404

    # test routes from whiskyton/blueprints/files.py

    def test_create_chart(self):
        db.session.add(self.whisky_1)
        db.session.add(self.whisky_2)
        db.session.add(self.correlation_1)
        db.session.add(self.correlation_2)
        db.session.commit()
        chart = Chart(reference=self.whisky_1, comparison=self.whisky_2)
        cache_name = chart.cache_name(True)
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
        db.session.add(self.whisky_1)
        db.session.add(self.whisky_2)
        db.session.commit()
        resp = self.app.get('/whiskyton.json')
        assert resp.status_code == 200

    def test_robots(self):
        resp = self.app.get('/robots.txt')
        assert resp.status_code in [200, 304]

    def test_favicon(self):
        resp = self.app.get('/favicon.ico')
        assert resp.status_code in [200, 304]

    def test_sitemap(self):
        db.session.add(self.whisky_1)
        db.session.add(self.whisky_2)
        db.session.commit()
        resp = self.app.get('/sitemap.xml')
        assert resp.status_code == 200
