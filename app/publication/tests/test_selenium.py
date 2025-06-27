import unittest
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager


@pytest.mark.selenium
class PublicationSeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(3)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_publish_labyrinth(self):
        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)

        self.driver.find_element(By.NAME, "username").send_keys("user1")
        self.driver.find_element(By.NAME, "password").send_keys("complexpass")
        self.driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Discover labyrinths").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Design labyrinth").click()
        time.sleep(1)
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "labyrinth.json"))
        self.driver.find_element(By.ID, "import-json").send_keys(json_path)
        time.sleep(1)

        self.driver.find_element(By.ID, "title").send_keys("Test Labyrinth")
        self.driver.find_element(By.ID, "description").send_keys("This is a test labyrinth.")
        self.driver.find_element(By.ID, "create").click()
        time.sleep(1)

        self.driver.find_elements(By.CLASS_NAME, "labyrinth-card-link")[-1].click()
        time.sleep(1)

        self.driver.find_element(By.ID, "publish").click()
        time.sleep(1)
        Alert(self.driver).accept()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Login").click()
        time.sleep(1)
        self.driver.find_element(By.NAME, "username").send_keys("user2")
        self.driver.find_element(By.NAME, "password").send_keys("complexpass")
        self.driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Discover labyrinths").click()
        time.sleep(1)
        self.driver.find_elements(By.CLASS_NAME, "labyrinth-card-link")[-1].click()
        time.sleep(1)

        self.driver.find_element(By.ID, "print").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "export").click()
        time.sleep(1)

        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="2"][data-col="1"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="2"][data-col="2"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="3"][data-col="2"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="4"][data-col="2"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="5"][data-col="2"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="5"][data-col="3"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="5"][data-col="4"]').click()
        self.driver.find_element(By.CSS_SELECTOR, 'td[data-row="5"][data-col="5"]').click()
        time.sleep(1)
        self.driver.find_element(By.ID, "solve").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "hide").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "reset").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
