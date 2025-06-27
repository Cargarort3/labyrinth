import unittest
import uuid
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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

    def test_register_and_login(self):
        username = f"testuser_{uuid.uuid4().hex[:8]}"
        password = "testpassword"

        self.driver.get("http://localhost:5000")
        self.driver.find_element(By.LINK_TEXT, "Register").click()
        time.sleep(1)

        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)

        self.driver.find_element(By.NAME, "username").send_keys(username)
        self.driver.find_element(By.NAME, "password").send_keys(password)
        self.driver.find_element(By.TAG_NAME, "form").submit()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "My profile").click()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
