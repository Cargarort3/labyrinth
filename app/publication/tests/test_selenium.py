import unittest
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager


@pytest.mark.selenium
class AuthSeleniumTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        options = Options()
        cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        cls.driver.implicitly_wait(3)
        cls.driver.maximize_window()

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_manage_labyrinth(self):
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
        self.driver.find_element(By.ID, "generator").click()
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
        self.driver.find_element(By.LINK_TEXT, "Discover labyrinths").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
