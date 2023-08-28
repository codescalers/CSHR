"""Module to test Update User Vacation Balance functionality."""
import pytest
from pages.add_office import Login, Office


def to_login(browse):
    """Function to login in tests."""
    login_page = Login(browse)
    login_page.enter_email("A@test.cs")
    login_page.enter_password("123456789")
    login_button = login_page.click_login_button()
    login_button.click()


@pytest.mark.parametrize("name, country", [
    ("جديد", "هليوبليس"),
    ("a", "online"),
    ("123", "111"),
    ("new_office", "هليوبليس"),
    ("front end", "nasr city"),
])
def test_new_office(browse, name, country):
    """Function to test name and country of office."""
    to_login(browse)
    office_page = Office(browse)
    office_page.click_dashboard_button()
    office_page.enter_office_name(name)
    office_page.enter_office_country(country)
    office_page.click_weekend_holidays()
    office_page.click_selected_weekend_holiday()
    submit_button = office_page.get_submit_button()
    assert submit_button.is_enabled()


def test_weekend_holidays_selection(browse):
    """Function to test weekend holidays selection of new office."""
    to_login(browse)
    office_page = Office(browse)
    office_page.click_dashboard_button()
    office_page.click_weekend_holidays()
    selected_holiday_name = office_page.get_selected_holiday_name()
    name_of_selected_holiday = selected_holiday_name.text
    office_page.click_selected_weekend_holiday()
    holiday_name_button = office_page.get_holiday_name_button()
    assert name_of_selected_holiday in holiday_name_button.text
