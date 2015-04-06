__author__ = 'cloverchio'

"""
Simple selenium regression suite for the UI.
To keep things simple, for now this suite uses a local instance of the FireFox driver
and is not ran on the grid.

https://github.com/cloverchio

"""

from selenium import webdriver
import unittest


class TitleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://whiskyton.herokuapp.com/")

    def testTitle(self):
        self.assertEqual(self.driver.title, "Whiskyton")

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class ContentTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://whiskyton.herokuapp.com/")

    def testContent(self):
        page_content = self.driver.page_source
        welcome_message = "Welcome, whisky lover!"
        self.assertTrue(welcome_message in page_content)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class SearchBarTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://whiskyton.herokuapp.com/")

    def testSearchVisibility(self):
        search_bar_text = "Tell us a whisky distillery you like"
        page_content = self.driver.page_source
        self.assertTrue(search_bar_text in page_content)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()

