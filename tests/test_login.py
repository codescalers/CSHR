"""Module to test login page."""
import pytest
from pages.login import Login


def test_user_login(browse):
    """test for login."""
    login_page = Login(browse)
    # Enter email
    login_page.enter_email("A@test.cs")
    # Enter password
    login_page.enter_password("123456789")
    # Click on Login button
    login_button = login_page.click_login_button()
    login_button.click()
    # Get the  profile
    profile = login_page.get_profile()
    # Assert that the element includes the text "AW"
    assert "aw" in profile.text.lower()


@pytest.mark.parametrize("email, passw", zip(Login.emails, Login.passwords))
def test_invalid_login(browse, email, passw):
    """test for invalid login."""
    login_page = Login(browse)
    login_page.enter_email(email)
    # Enter invalid password
    login_page.enter_password(passw)
    # Click on Login button
    login_button = login_page.click_login_button()
    login_button.click()
    assert login_button.is_enabled()


@pytest.mark.parametrize("email", Login.invalid_emails)
def test_email_validation(browse, email):
    """test for email validation."""
    login_page = Login(browse)
    # Enter email invalid email
    login_page.enter_email(email)
    # get the error message
    undefined_message = login_page.get_undefined_message()
    actual_text = undefined_message.text
    expected_text = "undefined"
    assert actual_text == expected_text
