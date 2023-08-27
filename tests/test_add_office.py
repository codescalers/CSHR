"""Module to test Update User Vacation Balance functionality."""
import time
from selenium import webdriver
import pytest
from pages.evaluation import Login, Office
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


def to_dashboard(driver1):
    """Function to go to dashboard page in tests."""
    dashboard_button = driver1.find_element(*Office.dashboard_button)
    dashboard_button.click()
    time.sleep(3)


@pytest.mark.parametrize("name, country", [
    ("جديد", "هليوبليس"),
    ("a", "online"),
    ("123", "111"),
    ("new_office", "هليوبليس"),
    ("front end", "nasr city"),
])
def test_new_office(driver1, name, country):
    """Function to test name and country of office."""
    to_login(driver1)
    to_dashboard(driver1)
    office_name = driver1.find_element(*Office.office_name)
    office_name.click()
    office_name.send_keys(name)
    office_country = driver1.find_element(*Office.office_country)
    office_country.click()
    office_country.send_keys(country)
    weekend_holidays = driver1.find_element(*Office.weekend_holidays)
    weekend_holidays.click()
    selected_weekend = driver1.find_element(*Office.selected_weekend_holiday)
    selected_weekend.click()
    submit_button = driver1.find_element(*Office.submit_button)
    assert submit_button.is_enabled()


def test_weekend_holidays_selection(driver1):
    """Function to test weekend holidays selection of new office."""
    to_login(driver1)
    to_dashboard(driver1)
    weekend_holidays = driver1.find_element(*Office.weekend_holidays)
    weekend_holidays.click()
    selected_holiday_name = driver1.find_element(*Office.selected_holiday_name)
    name_of_selected_holiday = selected_holiday_name.text
    selected_weekend = driver1.find_element(*Office.selected_weekend_holiday)
    selected_weekend.click()
    holiday_name_button = driver1.find_element(*Office.holiday_name_button)
    assert name_of_selected_holiday in holiday_name_button.text
