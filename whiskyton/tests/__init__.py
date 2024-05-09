from unittest import TestCase

from crates import all_whiskies

from whiskyton import create_app
from whiskyton.models import Whisky


class WhiskytonTest(TestCase):
    def setUp(self):
        app = create_app()
        app.config["TESTING"] = True
        app.config["WTF_CSRF_ENABLED"] = False
        self.app = app
        self.client = app.test_client()

        self.test_path = app.config["BASEDIR"] / "whiskyton" / "tests"
        self.whiskies = tuple(Whisky(*args) for args in all_whiskies())
