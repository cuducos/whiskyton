__author__ = "cloverchio"

"""
Simple selenium regression suite for the UI.
To keep things simple for now, this suite uses a local instance of the FireFox
driver and is not ran on the grid.

https://github.com/cloverchio

"""

from unittest import TestCase

from decouple import config
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

url = config("LOCAL_URL", default="http://localhost:5000/")


class UrlEndsWith:
    def __init__(self, value):
        self.value = value

    def __call__(self, driver):
        return driver.current_url.endswith(self.value)


class TestValidInput(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_valid_input(self):
        search_bar = self.driver.find_element_by_id("s")
        search_bar.clear()
        search_bar.send_keys("Aberlour")
        search_bar.submit()
        self.driver.implicitly_wait(20)
        xpath = "/html/body/div[1]/div[2]/div[2]"
        search_result = self.driver.find_elements_by_xpath(xpath)
        self.assertTrue(search_result)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class TestInvalidInput(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_invalid_input(self):
        search_bar = self.driver.find_element_by_id("s")
        search_bar.clear()
        search_bar.send_keys("foobar")
        search_bar.submit()
        WebDriverWait(self.driver, 20).until(UrlEndsWith("/search?s=foobar"))
        self.assertIn("Sorry, no whisky found", self.driver.page_source)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class TestRecommendSearch(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get(url)

    def test_option_list(self):
        search_bar = self.driver.find_element_by_id("s")
        search_bar.clear()
        search_bar.send_keys(" ")
        self.driver.implicitly_wait(20)
        xpath_1 = "/html/body/div[2]/div[5]"
        list_option = self.driver.find_element_by_xpath(xpath_1)
        list_option.click()
        search_bar.submit()
        self.driver.implicitly_wait(20)
        xpath_2 = "/html/body/div[1]/div[2]/div[2]"
        search_result = self.driver.find_elements_by_xpath(xpath_2)
        self.assertTrue(search_result)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
