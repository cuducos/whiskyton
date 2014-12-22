# coding: utf-8

from json import loads
from pyquery import PyQuery
from unittest import TestCase
from whiskyton import app, db
from whiskyton.helpers.charts import Chart
from whiskyton.models import Whisky
from whiskyton.tests.config import WhiskytonTest


class TestRoutes(TestCase):

    def setUp(self):
        self.test_suite = WhiskytonTest()
        self.app = self.test_suite.set_app(app, db)

    def tearDown(self):
        self.test_suite.unset_app(db)

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
