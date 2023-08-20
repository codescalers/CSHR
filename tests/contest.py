import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    driver.get("https://cshr.gent01.dev.grid.tf")
    return driver

