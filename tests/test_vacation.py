"""Module to test Update User Vacation Balance functionality."""
import time
from selenium import webdriver
import pytest
from pages.vacation import Login, Vacation, Employees
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


def to_select_user(driver1):
    """Function to select user in tests."""
    time.sleep(3)
    dashboard_button = driver1.find_element(*Vacation.dashboard_button)
    dashboard_button.click()
    time.sleep(3)
    button = driver1.find_element(*Vacation.users_button)
    button.click()
    time.sleep(3)
    random_user = driver1.find_element(*Vacation.random_user)
    random_user.click()


def test_update_of_user_vacation_balance(driver1):
    """Function to test update of user vacation balance."""
    to_login(driver1)
    time.sleep(3)
    to_select_user(driver1)
    load_balanc_button = driver1.find_element(*Vacation.load_balanc_butt)
    load_balanc_button.click()
    time.sleep(3)
    leave_execuses = driver1.find_element(*Vacation.leave_execuses)
    leave_execuses.click()
    leave_execuses.send_keys(Employees.leave_number)
    annual_leaves = driver1.find_element(*Vacation.annual_leaves)
    annual_leaves.click()
    annual_leaves.send_keys(Employees.annual_number)
    emergency_leaves = driver1.find_element(*Vacation.emergency_leaves)
    emergency_leaves.click()
    emergency_leaves.send_keys(Employees.emergency_number)
    delete_button = driver1.find_element(*Vacation.delete_old_balance_button)
    delete_button.click()
    time.sleep(3)
    submit_button = driver1.find_element(*Vacation.submit_button)
    submit_button.click()
    # go to employees page to check update
    employees_button = driver1.find_element(*Employees.employees_button)
    employees_button.click()
    time.sleep(3)
    random_profile = driver1.find_element(*Employees.random_profile)
    random_profile.click()
    time.sleep(3)
    annual_text = driver1.find_element(*Employees.annual_leaves_text)
    emergency_text = driver1.find_element(*Employees.emergency_leaves_text)
    leave_text = driver1.find_element(*Employees.leave_execus_text)
    is_annual = annual_text.text == Employees.annual_string
    is_emergency = emergency_text.text == Employees.emergency_string
    is_leave = leave_text.text == Employees.leave_string
    assert is_annual and is_emergency and is_leave


def test_name_of_the_user(driver1):
    """Function to test name of selected user."""
    to_login(driver1)
    time.sleep(3)
    to_select_user(driver1)
    random_user_name = driver1.find_element(*Vacation.random_user_name)
    user_name_in_selected_button = random_user_name.text
    load_balanc_button = driver1.find_element(*Vacation.load_balanc_butt)
    load_balanc_button.click()
    time.sleep(3)
    user_after_selected = driver1.find_element(*Vacation.user_name_selected)
    assert user_after_selected.text in user_name_in_selected_button


def test_check_load_balance_button(driver1):
    """Function to test load balance button."""
    to_login(driver1)
    time.sleep(3)
    to_select_user(driver1)
    load_balanc_button = driver1.find_element(*Vacation.load_balanc_butt)
    assert load_balanc_button.is_enabled()
    assert load_balanc_button.text == "Load Balance"


@pytest.mark.parametrize("annual, leave, emergency", [
    ("", "123", "456"),
    ("789", "", "456"),
    ("789", "123", ""),
])
def test_fields_with_empty(driver1, annual, leave, emergency):
    """Function to test load balance button."""
    to_login(driver1)
    to_select_user(driver1)
    load_balanc_button = driver1.find_element(*Vacation.load_balanc_butt)
    load_balanc_button.click()
    time.sleep(3)
    annual_leaves = driver1.find_element(*Vacation.annual_leaves)
    annual_leaves.click()
    annual_leaves.send_keys(annual)
    leave_execuses = driver1.find_element(*Vacation.leave_execuses)
    leave_execuses.click()
    leave_execuses.send_keys(leave)
    emergency_leaves = driver1.find_element(*Vacation.emergency_leaves)
    emergency_leaves.click()
    emergency_leaves.send_keys(emergency)
    submit_button = driver1.find_element(*Vacation.submit_button)
    if annual == "":
        error_message = driver1.find_element(*Vacation.annual_error_message)
        assert "Annual leaves is invalid" in error_message.text
        assert not submit_button.is_enabled()
    if leave == "":
        error_message = driver1.find_element(*Vacation.leave_error_message)
        assert "Leave execuses is invalid" in error_message.text
        assert not submit_button.is_enabled()
    if emergency == "":
        error_message = driver1.find_element(*Vacation.emergency_error_message)
        assert "Emergency leaves is invalid" in error_message.text
        assert not submit_button.is_enabled()
