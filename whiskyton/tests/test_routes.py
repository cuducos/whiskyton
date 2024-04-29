from json import loads

from pyquery import PyQuery

from whiskyton.helpers.charts import Chart
from whiskyton.models import Whisky
from whiskyton.tests.config import WhiskytonTest


class TestRoutes(WhiskytonTest):
    # test routes from whiskyton/blueprint/site.py

    def test_index(self):
        with self.app.app_context():
            resp = self.client.get("/")
            pq = PyQuery(resp.data)
            random = pq(".jumbotron strong").html()
            self.assertEqual(resp.status_code, 200)
            self.assertIn(random, ["Isle of Arran", "Glen Deveron / MacDuff"])

    def test_successful_search(self):
        with self.app.app_context():
            resp = self.client.get("/search?s=Glen+Deveron+%2F+MacDuff")
            self.assertEqual(resp.status_code, 302)

    def test_unsuccessful_search(self):
        with self.app.app_context():
            resp = self.client.get("/search?s=Bowm")
            pq = PyQuery(resp.data)
            title = pq("#whiskies h2").html()
            random = pq("#whiskies p a.label").html()
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Bowm", title)
            self.assertIn(random, ["Isle of Arran", "Glen Deveron / MacDuff"])

    def test_valid_whisky_page(self):
        with self.app.app_context():
            resp = self.client.get("/isleofarran")
            pq = PyQuery(resp.data)
            title = pq("#header h1").html()
            subtitle = pq("#whiskies h2 span.label").html()
            charts = pq("div.chart")
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Isle of Arran", title)
            self.assertIn("Isle of Arran", subtitle)
            self.assertTrue(charts)

    def test_invalid_whisky_page(self):
        with self.app.app_context():
            resp = self.client.get("/jackdaniels")
            pq = PyQuery(resp.data)
            form = pq("form")
            error_message = pq("#whiskies").html()
            self.assertEqual(resp.status_code, 404)
            self.assertIn("404", error_message)
            self.assertGreater(len(form), 0)

    def test_successful_search_id(self):
        with self.app.app_context():
            whisky = Whisky.query.first()
            resp = self.client.get("/w/{}".format(whisky.id))
            self.assertEqual(resp.status_code, 302)

    def test_unsuccessful_search_id(self):
        with self.app.app_context():
            resp = self.client.get("/w/{}".format(6.02e23))
            self.assertEqual(resp.status_code, 404)

    # test routes from whiskyton/blueprints/files.py

    def test_valid_chart(self):
        with self.app.app_context():
            whisky1, whisky2 = self.get_whiskies()
            chart = Chart(reference=whisky1, comparison=whisky2)
            cache_name = chart.cache_name(True)
            if cache_name.exists():
                cache_name.unlink()
            svg = "{}-{}.svg".format(whisky1.slug, whisky2.slug)
            resp = self.client.get("/charts/{}".format(svg))
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.data.decode("utf-8").count("<polygon "), 6)
            self.assertEqual(resp.data.decode("utf-8").count("<text "), 12)
            self.assertEqual(resp.data.decode("utf-8").count("<g "), 4)
            self.assertEqual(resp.data.decode("utf-8").count('id="grid"'), 1)
            self.assertEqual(resp.data.decode("utf-8").count('id="label"'), 1)
            self.assertEqual(resp.data.decode("utf-8").count('id="reference"'), 1)
            self.assertEqual(resp.data.decode("utf-8").count('id="whisky"'), 1)

    def test_invalid_chart(self):
        with self.app.app_context():
            resp = self.client.get("/charts/jackdaniels-jameson.svg")
            self.assertEqual(resp.status_code, 404)

    def test_whisky_json(self):
        with self.app.app_context():
            whisky1, whisky2 = self.get_whiskies()
            resp = self.client.get("/whiskyton.json")
            json_data = loads(resp.data)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("whiskies", json_data.keys())
            self.assertIn(whisky1.distillery, json_data["whiskies"])
            self.assertIn(whisky2.distillery, json_data["whiskies"])

    def test_robots(self):
        with self.app.app_context():
            resp = self.client.get("/robots.txt")
            self.assertIn(resp.status_code, [200, 304])

    def test_favicon(self):
        with self.app.app_context():
            resp = self.client.get("/favicon.ico")
            self.assertIn(resp.status_code, [200, 304])

    def test_sitemap(self):
        with self.app.app_context():
            resp = self.client.get("/sitemap.xml")
            self.assertIn(resp.status_code, [200, 304])
