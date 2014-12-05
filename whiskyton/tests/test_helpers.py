# coding: utf-8

import unittest
from datetime import datetime
from whiskyton import app
from whiskyton.helpers import sitemap
from whiskyton.helpers.charts import Chart
from whiskyton.models import Whisky


class TestHelpers(unittest.TestCase):

    def setUp(self):

        # init
        app.testing = True
        self.app = app.test_client()
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
            longitude=659720
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
            longitude=860400
        )

    def tearDown(self):
        pass

    # test methods from Whisky (whiskyton/models.py)

    def test_slug(self):
        assert self.whisky_2.get_slug() == 'glendeveronmacduff'

    def test_get_tastes(self):
        assertion = ['2', '2', '0', '1', '3', '2', '2', '2', '1', '1', '1', '1']
        assert self.whisky_1.get_tastes() == assertion

    # test methods from Chart (whiskyton/helpers/charts.py)

    def test_cache_path(self):
        cache_path = app.config['BASEDIR'] + '/whiskyton/static/charts'
        assert cache_path == (Chart()).cache_path()

    def test_cache_name(self):
        chart = Chart(reference=self.whisky_1, comparison=self.whisky_2)
        cache_dir_path = chart.cache_path()
        cache_file_path = chart.cache_name(True)
        cache_name = chart.cache_name()
        assertion = '220132221111x111113210202.svg'
        assert cache_name == assertion
        assert cache_file_path == cache_dir_path.child(cache_name).absolute()

    def test_create_and_cache(self):
        chart = Chart(reference=self.whisky_1, comparison=self.whisky_2)
        contents = chart.create()
        cached = chart.cache()
        assert contents == cached.read_file()

    # test methods from whiskyton/helpers/sitemap.py

    def test_recursive_listdir(self):
        sample_dir = app.config['BASEDIR'].child('whiskyton')
        files = sitemap.recursive_listdir(sample_dir)
        self.assertIsInstance(files, list)
        for file_path in files:
            assert file_path.exists()
            assert file_path.isfile()

    def test_most_recent_update(self):
        output = sitemap.most_recent_update()
        dt = datetime.strptime(output, '%Y-%m-%d')
        self.assertIsInstance(dt, datetime)
