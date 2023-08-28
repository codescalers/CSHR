"""Module to test Update User Vacation Balance functionality."""
import time
import pytest
from pages.vacation import Login, Vacation, Employees


def to_login(browse):
    """Function to login in tests."""
    login_page = Login(browse)
    login_page.enter_email("A@test.cs")
    login_page.enter_password("123456789")
    login_button = login_page.click_login_button()
    login_button.click()


def to_select_user(browse):
    """Function to select user in tests."""
    vacation_page = Vacation(browse)
    vacation_page.click_dashboard_button()
    vacation_page.click_users_button()
    vacation_page.click_random_user()


def test_update_of_user_vacation_balance(browse):
    """Function to test update of user vacation balance."""
    to_login(browse)
    time.sleep(3)
    to_select_user(browse)
    vacation_page = Vacation(browse)
    vacation_page.click_load_balance_button()
    vacation_page.enter_leave_execuses(Employees.leave_number)
    vacation_page.enter_annual_leaves(Employees.annual_number)
    vacation_page.enter_emergency_leaves(Employees.emergency_number)
    vacation_page.click_delete_old_balance_button()
    vacation_page.click_submit_button()

    employees_page = Employees(browse)
    employees_page.click_employees_button()

    employees_page.click_random_profile()

    annual_text = employees_page.get_annual_leaves_text()
    emergency_text = employees_page.get_emergency_leaves_text()
    leave_text = employees_page.get_leave_execus_text()

    is_annual = annual_text == Employees.annual_string
    is_emergency = emergency_text == Employees.emergency_string
    is_leave = leave_text == Employees.leave_string

    assert is_annual and is_emergency and is_leave


def test_name_of_the_user(browse):
    """Function to test name of selected user."""
    to_login(browse)
    to_select_user(browse)
    vacation_page = Vacation(browse)
    random_user_name = vacation_page.get_random_user_name()
    user_name_in_selected_button = random_user_name.text
    load_balanc_button = vacation_page.get_load_balanc_button()
    load_balanc_button.click()
    user_after_selected = vacation_page.get_user_after_selected()
    assert user_after_selected.text in user_name_in_selected_button


def test_check_load_balance_button(browse):
    """Function to test load balance button."""
    to_login(browse)
    to_select_user(browse)
    vacation_page = Vacation(browse)
    load_balanc_button = vacation_page.get_load_balanc_button()
    assert load_balanc_button.is_enabled()
    assert load_balanc_button.text == "Load Balance"


@pytest.mark.parametrize("annual, leave, emergency", [
    ("", "123", "456"),
    ("789", "", "456"),
    ("789", "123", ""),
])
def test_fields_with_empty(browse, annual, leave, emergency):
    """Function to test load balance button."""
    to_login(browse)
    to_select_user(browse)
    vacation_page = Vacation(browse)
    load_balanc_button = vacation_page.get_load_balanc_button()
    load_balanc_button.click()
    annual_leaves = vacation_page.get_annual_leaves()
    annual_leaves.click()
    annual_leaves.send_keys(annual)
    leave_execuses = vacation_page.get_leave_execuses()
    leave_execuses.click()
    leave_execuses.send_keys(leave)
    emergency_leaves = vacation_page.get_emergency_leaves()
    emergency_leaves.click()
    emergency_leaves.send_keys(emergency)
    submit_button = vacation_page.get_submit_button()
    if annual == "":
        error_message = vacation_page.get_annual_error_message()
        assert "Annual leaves is invalid" in error_message.text
        assert not submit_button.is_enabled()

    if leave == "":
        error_message = vacation_page.get_leave_error_message()
        assert "Leave execuses is invalid" in error_message.text
        assert not submit_button.is_enabled()

    if emergency == "":
        error_message = vacation_page.get_emergency_error_message()
        assert "Emergency leaves is invalid" in error_message.text
        assert not submit_button.is_enabled()
