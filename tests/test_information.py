"""Module to test Update User Vacation Balance functionality."""
from pages.information import lnformation
from pages.login import Login
from utils.config import LOGIN_PASSWORD


def setup_for_test(browse):
    """Function to login in tests."""
    login_page = Login(browse)
    login_page.enter_email(login_page.my_email)
    login_page.enter_password(LOGIN_PASSWORD)
    login_page.click_login_button()
    lnformation_page = lnformation(browse)
    lnformation_page.click_settings_button()
    return lnformation_page


def add_skill(browse, skill_name):
    lnformation_page = lnformation(browse)
    lnformation_page.input_add_new_skill(skill_name)
    lnformation_page.click_add_skill_button()
    lnformation_page.click_submit_button()
    message = lnformation_page.get_skill_add_message()
    assert "Skills Added!" in message.text


def test_add_skill(browse):
    lnformation_page = setup_for_test(browse)
    lnformation_page.input_add_new_skill("java")
    lnformation_page.click_add_skill_button()
    lnformation_page.click_submit_button()
    message = lnformation_page.get_skill_add_message()
    assert "Skills Added!" in message.text
    lnformation_page.click_profile_icon()
    p_elements = lnformation_page.get_p_elements()
    for p in p_elements:
        if "java" in p.text:
            assert True


def test_add_skill_already_is_skills(browse):
    lnformation_page = setup_for_test(browse)
    skill_name = "java"
    add_skill(browse, skill_name)
    lnformation_page.click_profile_icon()
    lnformation_page.click_settings_button()
    add_skill(browse, skill_name)
    lnformation_page.click_profile_icon()
    number_of_same_skill_in_profile = 0
    p_elements = lnformation_page.get_p_elements()
    for p in p_elements:
        if skill_name in p.text:
            number_of_same_skill_in_profile += 1
    assert number_of_same_skill_in_profile == 1
