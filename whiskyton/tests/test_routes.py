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
        resp = self.app.get('/')
        pq = PyQuery(resp.data)
        random = pq('.jumbotron strong').html()
        assert resp.status_code == 200
        assert random == 'Isle of Arran' or random == 'Glen Deveron / MacDuff'

    def test_successful_search(self):
        resp = self.app.get('/search?s=Glen+Deveron+%2F+MacDuff')
        assert resp.status_code == 302

    def test_unsuccessful_search(self):
        resp = self.app.get('/search?s=Bowm')
        pq = PyQuery(resp.data)
        title = pq('#whiskies h2').html()
        random = pq('#whiskies p a.label').html()
        assert resp.status_code == 200
        assert 'Bowm' in title
        assert random == 'Isle of Arran' or random == 'Glen Deveron / MacDuff'

    def test_valid_whisky_page(self):
        resp = self.app.get('/isleofarran')
        pq = PyQuery(resp.data)
        title = pq('#header h1').html()
        subtitle = pq('#whiskies h2 span.label').html()
        charts = pq('div.chart')
        assert resp.status_code == 200
        assert 'Isle of Arran' in title
        assert 'Isle of Arran' in subtitle
        assert charts

    def test_invalid_whisky_page(self):
        resp = self.app.get('/jackdaniels')
        pq = PyQuery(resp.data)
        form = pq('form')
        error_message = pq('#whiskies').html()
        assert resp.status_code == 404
        assert '404' in error_message
        assert len(form) > 0

    def test_successful_search_id(self):
        whisky = Whisky.query.first()
        resp = self.app.get('/w/{}'.format(whisky.id))
        assert resp.status_code == 302

    def test_unsuccessful_search_id(self):
        resp_2 = self.app.get('/w/{}'.format(6.02e+23))
        assert resp_2.status_code == 404

    # test routes from whiskyton/blueprints/files.py

    def test_valid_chart(self):
        whisky_1, whisky_2 = self.test_suite.get_whiskies()
        chart = Chart(reference=whisky_1, comparison=whisky_2)
        cache_name = chart.cache_name(True)
        if cache_name.exists():
            cache_name.remove()
        svg = '{}-{}.svg'.format(whisky_1.slug, whisky_2.slug)
        resp = self.app.get('/charts/{}'.format(svg))
        assert resp.status_code == 200
        assert resp.data.count('<polygon ') == 6
        assert resp.data.count('<text ') == 12
        assert resp.data.count('<g ') == 4
        assert resp.data.count('id="grid"') == 1
        assert resp.data.count('id="label"') == 1
        assert resp.data.count('id="reference"') == 1
        assert resp.data.count('id="whisky"') == 1

    def test_invalid_chart(self):
        resp = self.app.get('/charts/jackdaniels-jameson.svg')
        assert resp.status_code == 404

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
        whisky_1, whisky_2 = self.test_suite.get_whiskies()
        resp = self.app.get('/whiskyton.json')
        json_data = loads(resp.data)
        assert resp.status_code == 200
        assert 'whiskies' in json_data.keys()
        assert whisky_1.distillery in json_data['whiskies']
        assert whisky_2.distillery in json_data['whiskies']

    def test_robots(self):
        resp = self.app.get('/robots.txt')
        assert resp.status_code in [200, 304]

    def test_favicon(self):
        resp = self.app.get('/favicon.ico')
        assert resp.status_code in [200, 304]

    def test_sitemap(self):
        resp = self.app.get('/sitemap.xml')
        assert resp.status_code in [200, 304]
