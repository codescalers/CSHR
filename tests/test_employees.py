"""Module to test meeting page."""
from pages.Employees import Login, Employees


def to_login(browse):
    """Function to login in tests."""
    login_page = Login(browse)
    login_page.enter_email(login_page.my_email)
    login_page.enter_password("123456789")
    login_button = login_page.click_login_button()
    login_button.click()


def test_employees_displayed_on_page(browse):
    """test for all Employees ."""
    to_login(browse)
    employees_page = Employees(browse)
    employees_page.click_dashboard_button()
    all_present = employees_page.is_profile_present(Employees.profile_names)
    assert all_present


def test_employee_information_displayed(browse):
    """test for employee information ."""
    to_login(browse)
    employees_page = Employees(browse)
    employees_page.click_dashboard_button()
    random_profile_email = employees_page.get_random_prfile_email().text
    employees_page.click_random_profile()
    profile = employees_page.get_profile_email()
    assert profile.text == random_profile_email


def test_employee_information_accuracy(browse):
    """test for my profile ."""
    to_login(browse)
    login_page = Login(browse)
    my_login_email = login_page.my_email
    employees_page = Employees(browse)
    employees_page.click_dashboard_button()
    employees_page.click_my_profile()
    my_profile_email = employees_page.get_my_profile_email()
    assert my_profile_email.text == my_login_email
