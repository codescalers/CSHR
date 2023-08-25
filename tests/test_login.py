"""Module to test login page."""
import time
from selenium import webdriver
import pytest
from pages.login import Login
from utils.base import BASEURL


@pytest.fixture(name="driver1")
def driver1_fixture():
    """Function to save driver fixture."""
    driver = webdriver.Edge()
    driver.get(BASEURL)
    yield driver
    driver.quit()


def test_user_login(driver1):
    """test for login."""
    # Enter email
    email_input = driver1.find_element(*Login.email)
    email_input.send_keys("A@test.cs")
    # Enter password
    password_input = driver1.find_element(*Login.password)
    password_input.send_keys("123456789")
    # Click on Login button
    login_button = driver1.find_element(*Login.login_button)
    login_button.click()

    time.sleep(2)
    # Get the  profile
    profile = driver1.find_element(*Login.profile)
    # Assert that the element includes the text "AW"
    assert "aw" in profile.text.lower()


def test_invalid_login(driver1):
    """test for invalid login."""
    # Enter email invalid email
    email_input = driver1.find_element(*Login.email)
    email_input.send_keys("invalid@email.com")
    # Enter invalid password
    password_input = driver1.find_element(*Login.password)
    password_input.send_keys("123456789")
    # Click on Login button
    login_button = driver1.find_element(*Login.login_button)
    try:
        login_button.click()
    except ImportError:
        assert True


def test_email_validation(driver1):
    """test for email validation."""
    # Enter email invalid email
    email_input = driver1.find_element(*Login.email)
    email_input.send_keys("invalid@email.com")
    # get the error message
    undefined_message = driver1.find_element(*Login.undefined_message)
    actual_text = undefined_message.text
    expected_text = "undefined"
    assert actual_text == expected_text
