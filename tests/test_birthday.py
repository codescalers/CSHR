"""Module to test meeting page."""
from pages.birthday import Login, Birthday


def to_login(browse):
    """Function to login in tests."""
    login_page = Login(browse)
    # Enter email
    login_page.enter_email("A@test.cs")
    # Enter password
    login_page.enter_password("123456789")
    # Click on Login button
    login_button = login_page.click_login_button()
    login_button.click()


def test_display_of_birthday_icon(browse):
    """Function to test birthday."""
    to_login(browse)
    birthday_page = Birthday(browse)
    birthday_button = birthday_page.get_birthday_button()
    button_text = birthday_button.text
    assert "🎂 BIRTHDAY" == button_text
