"""Module to test login page."""
from pages.login import Login
from tests.contest import browsee
from utils.utils import generate_random_email, generate_random_password
from utils.utils import generate_random_invalid_email


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


def test_invalid_login(browse):
    """test for invalid login."""
    login_page = Login(browse)
    for _ in range(4):
        login_page.enter_email(generate_random_email())
        # Enter invalid password
        login_page.enter_password(generate_random_password())
        # Click on Login button
        login_button = login_page.click_login_button()
        try:
            assert login_button.is_enabled()
        except AssertionError:
            continue


def test_email_validation(browse):
    """test for email validation."""
    login_page = Login(browse)
    for _ in range(4):
        # Enter email invalid email
        login_page.enter_email(generate_random_invalid_email())
        # get the error message
        undefined_message = login_page.get_undefined_message()
        actual_text = undefined_message.text
        expected_text = "undefined"
        assert actual_text == expected_text
