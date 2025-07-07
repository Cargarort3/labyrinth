import unittest
import pytest
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.alert import Alert
from webdriver_manager.chrome import ChromeDriverManager


@pytest.mark.selenium
class LabyrinthSeleniumTest(unittest.TestCase):
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

        self.driver.find_element(By.LINK_TEXT, "Design a labyrinth").click()
        time.sleep(1)
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "labyrinth.json"))
        self.driver.find_element(By.ID, "import-json").send_keys(json_path)
        time.sleep(1)
        self.driver.find_element(By.ID, "rows").clear()
        self.driver.find_element(By.ID, "rows").send_keys("30")
        self.driver.find_element(By.ID, "cols").clear()
        self.driver.find_element(By.ID, "cols").send_keys("30")
        self.driver.find_element(By.ID, "adjust").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "reset").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "end-row").clear()
        self.driver.find_element(By.ID, "end-row").send_keys("30")
        self.driver.find_element(By.ID, "end-col").clear()
        self.driver.find_element(By.ID, "end-col").send_keys("30")
        self.driver.find_element(By.ID, "generator").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "solve").click()
        time.sleep(1)
        Select(self.driver.find_element(By.ID, "algorithm")).select_by_value("dfs")
        self.driver.find_element(By.ID, "solve").click()
        time.sleep(1)
        Select(self.driver.find_element(By.ID, "algorithm")).select_by_value("rw")
        time.sleep(1)
        self.driver.find_element(By.ID, "solve").click()
        time.sleep(3)
        self.driver.find_element(By.ID, "hide").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "print").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "export").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "title").send_keys("Test Labyrinth")
        self.driver.find_element(By.ID, "description").send_keys("This is a test labyrinth.")
        self.driver.find_element(By.ID, "create").click()
        time.sleep(1)

        self.driver.find_elements(By.CLASS_NAME, "labyrinth-card-link")[-1].click()
        time.sleep(1)
        self.driver.find_element(By.ID, "print").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "export").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "edit").click()
        time.sleep(1)
        json_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "labyrinth.json"))
        self.driver.find_element(By.ID, "import-json").send_keys(json_path)
        time.sleep(1)
        self.driver.find_element(By.ID, "rows").clear()
        self.driver.find_element(By.ID, "rows").send_keys("25")
        self.driver.find_element(By.ID, "cols").clear()
        self.driver.find_element(By.ID, "cols").send_keys("50")
        self.driver.find_element(By.ID, "adjust").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "reset").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "end-row").clear()
        self.driver.find_element(By.ID, "end-row").send_keys("25")
        self.driver.find_element(By.ID, "end-col").clear()
        self.driver.find_element(By.ID, "end-col").send_keys("50")
        self.driver.find_element(By.ID, "generator").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "solve").click()
        time.sleep(1)
        Select(self.driver.find_element(By.ID, "algorithm")).select_by_value("dfs")
        self.driver.find_element(By.ID, "solve").click()
        time.sleep(1)
        Select(self.driver.find_element(By.ID, "algorithm")).select_by_value("rw")
        time.sleep(1)
        self.driver.find_element(By.ID, "solve").click()
        time.sleep(3)
        self.driver.find_element(By.ID, "hide").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "print").click()
        time.sleep(1)
        self.driver.find_element(By.ID, "export").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "title").clear()
        self.driver.find_element(By.ID, "title").send_keys("Edited Test Labyrinth")
        self.driver.find_element(By.ID, "description").clear()
        self.driver.find_element(By.ID, "description").send_keys("This is an edited test labyrinth.")
        self.driver.find_element(By.ID, "edit").click()
        time.sleep(1)

        self.driver.find_element(By.ID, "delete").click()
        time.sleep(1)
        Alert(self.driver).accept()
        time.sleep(1)

        self.driver.find_element(By.LINK_TEXT, "Logout").click()
        time.sleep(1)
