from whiskyton.helpers.charts import Chart
from whiskyton.tests.config import WhiskytonTest


class TestHelpers(WhiskytonTest):
    # test methods from Whisky (whiskyton/models.py)

    def test_slug(self):
        with self.app.app_context():
            whisky = self.get_whisky(2)
            self.assertEqual(whisky.get_slug(), "glendeveronmacduff")

    def test_get_tastes(self):
        with self.app.app_context():
            whisky = self.get_whisky(2)
            tastes = ["1", "1", "1", "1", "1", "3", "2", "1", "0", "2", "0", "2"]
            self.assertEqual(whisky.get_tastes(), tastes)

    # test methods from Chart (whiskyton/helpers/charts.py)

    def test_cache_path(self):
        with self.app.app_context():
            base_dir = self.app.config["BASEDIR"]
            cache_path = base_dir / "whiskyton" / "static" / "charts"
            chart = Chart()
            self.assertEqual(cache_path, chart.cache_path())

    def test_cache_name(self):
        with self.app.app_context():
            whisky1, whisky2 = self.get_whiskies()
            chart = Chart(reference=whisky1, comparison=whisky2)
            cache_dir_path = chart.cache_path()
            cache_file_path = chart.cache_name(True)
            cache_name = chart.cache_name()
            self.assertEqual(cache_name, "110113221101x111113210202.svg")
            self.assertEqual(cache_file_path, (cache_dir_path / cache_name).absolute())

    def test_create_and_cache(self):
        with self.app.app_context():
            base_dir = self.app.config["BASEDIR"]
            whisky1, whisky2 = self.get_whiskies()
            chart = Chart(reference=whisky1, comparison=whisky2)
            contents = chart.create()
            cached = chart.cache()
            sample = base_dir / "whiskyton" / "tests" / "chart_sample.svg"
            self.assertEqual(contents, cached.read_text())
            self.assertEqual(contents, sample.read_text())
