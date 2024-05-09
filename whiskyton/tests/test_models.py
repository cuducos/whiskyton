from whiskyton.models import Chart
from whiskyton.tests import WhiskytonTest


class TestChart(WhiskytonTest):
    def test_create(self):
        with self.app.app_context():
            chart = Chart(
                reference=(2, 2, 3, 1, 0, 2, 2, 1, 1, 1, 1, 2),
                comparison=(2, 2, 3, 1, 0, 2, 1, 1, 1, 2, 1, 1),
            )
            contents = chart.create()
            sample = self.test_path / "chart_sample.svg"
            self.assertEqual(contents, sample.read_text())
