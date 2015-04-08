__author__ = 'cloverchio'

"""
Simple selenium regression suite for the UI.
To keep things simple for now, this suite uses a local instance of the FireFox driver
and is not ran on the grid.

https://github.com/cloverchio

"""

from selenium import webdriver
import unittest


class ValidInputTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://whiskyton.herokuapp.com/")

    def testValidInput(self):
        search_bar = self.driver.find_element_by_id('s')
        search_bar.clear()
        search_bar.send_keys("Aberlour")
        search_bar.submit()
        self.driver.implicitly_wait(20)
        search_result = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]")
        self.assertTrue(search_result.size > 0)
        self.assertFalse(search_result.size <= 0)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class InvalidInputTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://whiskyton.herokuapp.com/")

    def testInvalidInput(self):
        search_bar = self.driver.find_element_by_id('s')
        search_bar.clear()
        search_bar.send_keys(" ")
        search_bar.submit()
        self.driver.implicitly_wait(20)
        page_content = self.driver.page_source
        no_results_text = "Sorry, no whisky found"
        self.assertTrue(no_results_text in page_content)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


class RecommendSearchTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.driver = webdriver.Firefox()
        cls.driver.get("http://whiskyton.herokuapp.com/")

    def testOptionList(self):
        search_bar = self.driver.find_element_by_id('s')
        search_bar.clear()
        search_bar.send_keys(" ")
        self.driver.implicitly_wait(20)
        list_option = self.driver.find_element_by_xpath("/html/body/div[2]/div[5]")
        list_option.click()
        search_bar.submit()
        self.driver.implicitly_wait(20)
        search_result = self.driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[2]")
        self.assertTrue(search_result.size > 0)
        self.assertFalse(search_result.size <= 0)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()


if __name__ == "__main__":
    unittest.main()