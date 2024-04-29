from os import environ
from unittest import TestCase

from whiskyton import create_app
from whiskyton.models import Correlation, Whisky, db


class WhiskytonTest(TestCase):
    def setUp(self):
        environ["DATABASE_URL"] = "sqlite:///:memory:"
        app = create_app()

        # basic testing vars
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        # create tables and testing db data
        with app.app_context():
            whisky1, whisky2 = self.whisky1, self.whisky2
            db.create_all()
            db.session.add(whisky1)
            db.session.add(whisky2)
            db.session.commit()

            query1 = Whisky.query.filter(Whisky.slug == "isleofarran")
            query2 = Whisky.query.filter(Whisky.slug == "glendeveronmacduff")
            calc_correlation_1 = whisky1.get_correlation(query2.first())
            calc_correlation_2 = whisky2.get_correlation(query1.first())
            correlation1 = Correlation(**calc_correlation_1)
            correlation2 = Correlation(**calc_correlation_2)
            db.session.add(correlation1)
            db.session.add(correlation2)
            db.session.commit()

        self.app = app
        self.client = app.test_client()

    @property
    def whisky1(self):
        return Whisky(
            distillery="Isle of Arran",
            body=2,
            sweetness=3,
            smoky=1,
            medicinal=1,
            tobacco=0,
            honey=1,
            spicy=1,
            winey=1,
            nutty=0,
            malty=1,
            fruity=1,
            floral=2,
            postcode="KA27 8HJ",
            latitude=194050,
            longitude=649950,
            slug="isleofarran",
        )

    @property
    def whisky2(self):
        return Whisky(
            distillery="Glen Deveron / MacDuff",
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
            postcode="AB4 3JT",
            latitude=372120,
            longitude=860400,
            slug="glendeveronmacduff",
        )

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def get_whisky(self, whisky_id=1):
        return self.get_whiskies()[whisky_id - 1]

    def get_whiskies(self):
        return self.whisky1, self.whisky2
