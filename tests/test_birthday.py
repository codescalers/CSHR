"""Module to test meeting page."""
import time
from selenium import webdriver
import pytest
from pages.birthday import Login, Birthday
from utils.base import BASEURL


@pytest.fixture(name="driver1")
def driver1_fixture():
    """Function to save driver fixture."""
    driver = webdriver.Edge()
    driver.get(BASEURL)
    yield driver
    driver.quit()


def to_login(driver1):
    """Function to login in tests."""
    email_input = driver1.find_element(*Login.email)
    email_input.send_keys("A@test.cs")
    password_input = driver1.find_element(*Login.password)
    password_input.send_keys("123456789")
    login_button = driver1.find_element(*Login.login_button)
    login_button.click()
    time.sleep(3)


def test_display_of_birthday_icon(driver1):
    """Function to test birthday."""
    to_login(driver1)
    birthday_button = driver1.find_element(*Birthday.birthday_button)
    button_text = birthday_button.text
    assert "🎂 BIRTHDAY" == button_text
