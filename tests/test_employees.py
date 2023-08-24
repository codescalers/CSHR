"""Module to test meeting page."""
import time
from selenium import webdriver
import pytest
from pages.Employees import Login, Employees
from utils.base import BASEURL


@pytest.fixture(name="driver1")
def driver1_fixture():
    """Function to save driver fixture."""
    driver = webdriver.Edge()
    driver.get(BASEURL)
    yield driver
    driver.quit()


def to_login(driver1):
    """Function to login  then go to employees page in tests."""
    email_input = driver1.find_element(*Login.email)
    email_input.send_keys("A@test.cs")
    password_input = driver1.find_element(*Login.password)
    password_input.send_keys("123456789")
    login_button = driver1.find_element(*Login.login_button)
    login_button.click()
    time.sleep(2)


def employees_page(driver1):
    """Function to go to employees page in tests."""
    employees_button = driver1.find_element(*Employees.employees_button)
    employees_button.click()
    time.sleep(2)


def test_employees_displayed_on_page(driver1):
    """test for all Employees ."""
    to_login(driver1)
    employees_page(driver1)
    parent_element = driver1.find_element(*Employees.parent_element)
    profile_links = parent_element.find_elements(*Employees.profile_links)
    # Dictionary to track if the profile is present or not
    profile_presence = {}
    # Initialize the profile
    for name in Employees.profile_names:
        profile_presence[name] = False
    # Iterate through each profile link
    for link in profile_links:
        profile_element = link.find_element(*Employees.profile_text_element)
        profile_text = profile_element.text
        # Put value if existi
        profile_presence[profile_text] = True
    # Check if all profile names are present
    all_present = all(value for value in profile_presence.values())
    assert all_present


def test_employee_information_displayed(driver1):
    """test for employee information ."""
    to_login(driver1)
    employees_page(driver1)
    random_profile = driver1.find_element(*Employees.random_profile)
    random_profile.click()
    profile = driver1.find_element(*Employees.email_profile)
    assert profile.text == "admin@gmail.com"


def test_employee_information_accuracy(driver1):
    """test for my profile ."""
    to_login(driver1)
    employees_page(driver1)
    my_profile = driver1.find_element(*Employees.my_profile)
    my_profile.click()
    my_profile_email = driver1.find_element(*Employees.my_profile_email)
    assert my_profile_email.text == "A@test.cs"
