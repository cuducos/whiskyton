from json import loads

from pyquery import PyQuery

from whiskyton.tests import WhiskytonTest


class TestSiteRoutes(WhiskytonTest):
    def test_index(self):
        with self.app.app_context():
            resp = self.client.get("/")
            pq = PyQuery(resp.data)
            random = pq(".jumbotron strong").html()
            self.assertEqual(resp.status_code, 200)
            self.assertIn(random, (whisky.distillery for whisky in self.whiskies))

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
            self.assertIn(random, (whisky.distillery for whisky in self.whiskies))

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


class TestFilesRoutes(WhiskytonTest):
    def test_whisky_json(self):
        with self.app.app_context():
            resp = self.client.get("/whiskyton.json")
            data = loads(resp.data)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("whiskies", data.keys())
            for whisky in self.whiskies:
                self.assertIn(whisky.distillery, data["whiskies"])

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
            for whisky in self.whiskies:
                self.assertIn(whisky.slug, resp.text)
