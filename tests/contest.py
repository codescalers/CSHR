from selenium import webdriver
import pytest
from utils.base import BASEURL


@pytest.fixture(name="browse", scope="function")
def browsee():
    """Function to save driver fixture."""
    driver = webdriver.Edge()
    driver.get(BASEURL)
    yield driver
    driver.quit()
