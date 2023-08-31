from selenium import webdriver
import pytest
from utils.base import BASEURL


@pytest.fixture(name="browse", scope="function")
def browsee():
    """Function to save driver fixture."""
    browser = webdriver.Chrome()
    browser.get(BASEURL)
    yield browser
    browser.quit()
