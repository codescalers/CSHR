from selenium import webdriver
import pytest
from utils.base import BASEURL
from selenium.webdriver.chrome.options import Options


@pytest.fixture(name="browse", scope="function")
def browsee():
    """Function to save driver fixture."""
    options1 = Options()
    options1.add_argument("--reuse-browser-session")
    browser = webdriver.Chrome(options=options1)
    browser.get(BASEURL)
    yield browser
    browser.quit()
