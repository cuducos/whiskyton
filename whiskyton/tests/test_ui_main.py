"""
Simple selenium regression suite for the UI.
To keep things simple, for now this suite uses a local instance of the Firefox
driver and is not ran on the grid.

https://github.com/cloverchio
"""

from os import getenv
from unittest import TestCase

from selenium import webdriver

__author__ = "cloverchio"

url = getenv("LOCAL_URL", "http://localhost:5000/")


class TestTitle(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_title(self):
        self.assertEqual(self.driver.title, "Whiskyton")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class TestContent(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_content(self):
        page_content = self.driver.page_source
        welcome_message = "Welcome, whisky lover!"
        self.assertTrue(welcome_message in page_content)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class TestSearchBarTest(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_search_visibility(self):
        search_bar_text = "Tell us a whisky distillery you like"
        page_content = self.driver.page_source
        self.assertTrue(search_bar_text in page_content)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
