from json import loads
from unittest import TestCase

from pyquery import PyQuery

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
        resp = self.app.get("/")
        pq = PyQuery(resp.data)
        random = pq(".jumbotron strong").html()
        self.assertEqual(resp.status_code, 200)
        self.assertIn(random, ["Isle of Arran", "Glen Deveron / MacDuff"])

    def test_successful_search(self):
        resp = self.app.get("/search?s=Glen+Deveron+%2F+MacDuff")
        self.assertEqual(resp.status_code, 302)

    def test_unsuccessful_search(self):
        resp = self.app.get("/search?s=Bowm")
        pq = PyQuery(resp.data)
        title = pq("#whiskies h2").html()
        random = pq("#whiskies p a.label").html()
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Bowm", title)
        self.assertIn(random, ["Isle of Arran", "Glen Deveron / MacDuff"])

    def test_valid_whisky_page(self):
        resp = self.app.get("/isleofarran")
        pq = PyQuery(resp.data)
        title = pq("#header h1").html()
        subtitle = pq("#whiskies h2 span.label").html()
        charts = pq("div.chart")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("Isle of Arran", title)
        self.assertIn("Isle of Arran", subtitle)
        self.assertTrue(charts)

    def test_invalid_whisky_page(self):
        resp = self.app.get("/jackdaniels")
        pq = PyQuery(resp.data)
        form = pq("form")
        error_message = pq("#whiskies").html()
        self.assertEqual(resp.status_code, 404)
        self.assertIn("404", error_message)
        self.assertGreater(len(form), 0)

    def test_successful_search_id(self):
        whisky = Whisky.query.first()
        resp = self.app.get("/w/{}".format(whisky.id))
        self.assertEqual(resp.status_code, 302)

    def test_unsuccessful_search_id(self):
        resp = self.app.get("/w/{}".format(6.02e23))
        self.assertEqual(resp.status_code, 404)

    # test routes from whiskyton/blueprints/files.py

    def test_valid_chart(self):
        whisky_1, whisky_2 = self.test_suite.get_whiskies()
        chart = Chart(reference=whisky_1, comparison=whisky_2)
        cache_name = chart.cache_name(True)
        if cache_name.exists():
            cache_name.remove()
        svg = "{}-{}.svg".format(whisky_1.slug, whisky_2.slug)
        resp = self.app.get("/charts/{}".format(svg))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode("utf-8").count("<polygon "), 6)
        self.assertEqual(resp.data.decode("utf-8").count("<text "), 12)
        self.assertEqual(resp.data.decode("utf-8").count("<g "), 4)
        self.assertEqual(resp.data.decode("utf-8").count('id="grid"'), 1)
        self.assertEqual(resp.data.decode("utf-8").count('id="label"'), 1)
        self.assertEqual(resp.data.decode("utf-8").count('id="reference"'), 1)
        self.assertEqual(resp.data.decode("utf-8").count('id="whisky"'), 1)

    def test_invalid_chart(self):
        resp = self.app.get("/charts/jackdaniels-jameson.svg")
        self.assertEqual(resp.status_code, 404)

    def test_whisky_json(self):
        whisky_1, whisky_2 = self.test_suite.get_whiskies()
        resp = self.app.get("/whiskyton.json")
        json_data = loads(resp.data)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("whiskies", json_data.keys())
        self.assertIn(whisky_1.distillery, json_data["whiskies"])
        self.assertIn(whisky_2.distillery, json_data["whiskies"])

    def test_robots(self):
        resp = self.app.get("/robots.txt")
        self.assertIn(resp.status_code, [200, 304])

    def test_favicon(self):
        resp = self.app.get("/favicon.ico")
        self.assertIn(resp.status_code, [200, 304])

    def test_sitemap(self):
        resp = self.app.get("/sitemap.xml")
        self.assertIn(resp.status_code, [200, 304])
