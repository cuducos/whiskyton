from decouple import config

from whiskyton.models import Correlation, Whisky


class WhiskytonTest(object):
    def __init__(self):
        self.whisky_1 = Whisky(
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
            views=0,
        )
        self.whisky_2 = Whisky(
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
            views=0,
        )

    def set_app(self, app, db=False):

        # basic testing vars
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False

        # set db for tests
        if db:
            app.config["SQLALCHEMY_DATABASE_URI"] = config(
                "DATABASE_URL_TEST", default="sqlite://"
            )

        # create test app
        test_app = app.test_client()

        # create tables and testing db data
        if db:
            db.create_all()
            db.session.add(self.whisky_1)
            db.session.add(self.whisky_2)
            db.session.commit()
            query_1 = Whisky.query.filter(Whisky.slug == "isleofarran")
            query_2 = Whisky.query.filter(Whisky.slug == "glendeveronmacduff")
            calc_correlation_1 = self.whisky_1.get_correlation(query_2.first())
            calc_correlation_2 = self.whisky_2.get_correlation(query_1.first())
            correlation_1 = Correlation(**calc_correlation_1)
            correlation_2 = Correlation(**calc_correlation_2)
            db.session.add(correlation_1)
            db.session.add(correlation_2)
            db.session.commit()

        # return the text app
        return test_app

    @staticmethod
    def unset_app(db=False):

        # clean the db
        if db:
            db.session.remove()
            db.drop_all()

        return True

    def get_whisky(self, whisky_id=1):
        if whisky_id == 2:
            return self.whisky_2
        return self.whisky_1

    def get_whiskies(self):
        return self.whisky_1, self.whisky_2
