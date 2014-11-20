# coding: utf-8

import os
import unittest
from whiskyton import app, charts, db, whisky
from whiskyton.models import Whisky


class TestCase(unittest.TestCase):

    def setUp(self):

        # app settings
        app.config['TESTING'] = True

        # test db settings
        db_protocol = 'sqlite:///'
        db_path = app.config['BASEDIR'].child('test.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = db_protocol + db_path

        # init
        self.app = app.test_client()
        db.create_all()

        # some fake data to be used by tests
        app.config['W1'] = Whisky(
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
        app.config['W2'] = Whisky(
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
        db.session.remove()
        db.drop_all()

    # test functions of whiskyton/whisky.py

    def test_slug(self):
        assert whisky.slugfy('Glen Deveron / MacDuff') == 'glendeveronmacduff'

    # test functions of whiskyton/charts.py

    def test_tastes2list(self):
        w = app.config['W1']
        l = ['2', '2', '0', '1', '3', '2', '2', '2', '1', '1', '1', '1']
        assert charts.tastes2list(w) == l

    def test_cache_path(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        cache_path = basedir + '/whiskyton/static/charts'
        assert cache_path == charts.cache_path()

    def test_cache_name(self):
        # test data
        tastes_1 = ['2', '2', '3', '1', '0', '2', '2', '1', '1', '1', '1', '2']
        tastes_2 = ['2', '3', '1', '1', '1', '1', '1', '2', '0', '2', '0', '1']
        basedir = os.path.abspath(os.path.dirname(__file__))
        path = basedir + '/whiskyton/static/charts/'
        # app values
        cache_path = charts.cache_name(tastes_1, tastes_2, True)
        cache_name_1 = charts.cache_name(tastes_1, tastes_2, False)
        cache_name_2 = charts.cache_name(tastes_1, tastes_2)
        # test
        assert cache_name_1 == cache_name_2 == '223102211112x231111120201.svg'
        assert cache_path == path + cache_name_1

if __name__ == '__main__':
    unittest.main()
