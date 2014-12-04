# coding: utf-8

import unittest
from whiskyton import app
from whiskyton.helpers import charts, whisky
from whiskyton.models import Whisky


class TestHelpers(unittest.TestCase):

    def setUp(self):

        if 'BASEDIR_BKP' not in app.config:

            # replace config['BASEDIR'] with a directory for tests
            app.config['BASEDIR_BKP'] = app.config['BASEDIR']
            app.config['TESTS_DIR'] = app.config['BASEDIR'].child('tests')
            app.config['TESTS_DIR'].mkdir()
            app.config['BASEDIR'] = app.config['TESTS_DIR']

            # copy chart.svg template
            templates_dir = app.config['TESTS_DIR'].child('whiskyton', 'templates')
            chart_svg = app.config['BASEDIR_BKP'].child('whiskyton', 'templates', 'chart.svg')
            templates_dir.mkdir(True)
            chart_svg.copy(templates_dir.child(chart_svg.name))

        # init
        app.config['TESTING'] = True
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
            longitude=659720)
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
            longitude=860400)

    def tearDown(self):
        app.config['BASEDIR'] = app.config['BASEDIR_BKP']
        app.config['TESTS_DIR'].rmtree()

    # test functions of whiskyton/helpers/whisky.py

    def test_slug(self):
        assert whisky.slugfy('Glen Deveron / MacDuff') == 'glendeveronmacduff'

    # test functions of whiskyton/helpers/charts.py

    def test_tastes2list(self):
        assertion = ['2', '2', '0', '1', '3', '2', '2', '2', '1', '1', '1', '1']
        assert charts.tastes2list(self.whisky_1) == assertion

    def test_cache_path(self):
        cache_path = app.config['BASEDIR'] + '/whiskyton/static/charts'
        assert cache_path == charts.cache_path()

    def test_cache_name(self):
        tastes_1 = charts.tastes2list(self.whisky_1)
        tastes_2 = charts.tastes2list(self.whisky_2)
        cache_dir_path = charts.cache_path()
        cache_path = charts.cache_name(tastes_1, tastes_2, True)
        cache_name_1 = charts.cache_name(tastes_1, tastes_2, False)
        cache_name_2 = charts.cache_name(tastes_1, tastes_2)
        assertion = '220132221111x111113210202.svg'
        assert cache_name_1 == assertion
        assert cache_name_2 == assertion
        print cache_path
        print cache_dir_path + cache_name_1
        assert cache_path == cache_dir_path.child(cache_name_1).absolute()

    def test_create(self):
        tastes_1 = charts.tastes2list(self.whisky_1)
        tastes_2 = charts.tastes2list(self.whisky_2)
        slug_1 = whisky.slugfy(self.whisky_1.distillery)
        slug_2 = whisky.slugfy(self.whisky_2.distillery)
        charts.create(tastes_1, tastes_2)
        resp = self.app.get('/charts/{}-{}.svg'.format(slug_1, slug_2))
        assert resp.status_code == 200
