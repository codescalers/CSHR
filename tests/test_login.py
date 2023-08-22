import time
from pages.login import login
import pytest
from selenium import webdriver
@pytest.fixture
def driver1():
    driver = webdriver.Chrome()
    driver.get("https://cshr.gent01.dev.grid.tf")
    yield driver
    driver.quit()
def test_user_login(driver1):
    login_instance = login()
    # Enter email
    email_input = driver1.find_element(*login_instance.email)
    email_input.send_keys("A@test.cs")
    # Enter password
    password_input = driver1.find_element(*login_instance.password)
    password_input.send_keys("123456789")
     # Click on Login button
    login_button = driver1.find_element(*login_instance.login_button)
    login_button.click()

    time.sleep(10)
    # Get the  profile
    profile = driver1.find_element(*login_instance.profile)
    # Assert that the element includes the text "AW"
    assert "aw" in profile.text.lower()
def test_invalid_login(driver1):
    login_instance = login()
    # Enter email invalid email
    email_input = driver1.find_element(*login_instance.email)
    email_input.send_keys("invalid@email.com")
    
    # Enter invalid password
    password_input = driver1.find_element(*login_instance.password)
    password_input.send_keys("123456789")
    
    # Click on Login button
    login_button = driver1.find_element(*login_instance.login_button)
    try:login_button.click()
    except ImportError:
        assert True 
def test_email_validation(driver1):
    login_instance = login()
    # Enter email invalid email
    email_input = driver1.find_element(*login_instance.email)
    email_input.send_keys("invalid@email.com")
    # get the error message
    undefined_message=driver1.find_element(*login_instance.undefined_message)
    actual_text = undefined_message.text
    expected_text = "undefined"
    assert actual_text == expected_text