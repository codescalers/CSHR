"""Module to test Update User Vacation Balance functionality."""
import validators
import pytest
from pages.evaluation import Evaluation
from pages.login import Login
from utils.config import LOGIN_PASSWORD


def setup_for_test(browse):
    """Function to login in tests."""
    login_page = Login(browse)
    login_page.enter_email(login_page.my_email)
    login_page.enter_password(LOGIN_PASSWORD)
    login_page.click_login_button()
    evaluation_page = Evaluation(browse)
    evaluation_page.click_dashboard_button()
    return evaluation_page


def test_form_submission(browse):
    """Function to test submission of form."""
    evaluation_page = setup_for_test(browse)
    evaluation_page.click_select_user()
    evaluation_page.selected_usered()
    evaluation_page.select_evaluation_quartur()
    evaluation_page.select_quartur()
    evaluation_page.input_evaluation_link("link.com")
    evaluation_page.input_score_value(Evaluation.random_score_value)
    submit_button = evaluation_page.get_submit_button()
    assert submit_button.is_enabled()


def test_user_selection(browse):
    """Function to test user selection in form."""
    evaluation_page = setup_for_test(browse)
    evaluation_page.click_select_user()
    name_befor = evaluation_page.get_name_befor()
    name_befor = name_befor.text
    evaluation_page.selected_usered()
    name_after = evaluation_page.get_user_name_after_selected().text
    assert name_befor in name_after


def test_evaluation_quarter_selection(browse):
    """Function to test evaluation quarter selection in form."""
    evaluation_page = setup_for_test(browse)
    evaluation_page.select_evaluation_quartur()
    name_befor = evaluation_page.get_quartur_name_befor()
    name_befor = name_befor.text
    evaluation_page.select_quartur()
    name_after = evaluation_page.get_quartur_name_after().text
    assert name_befor in name_after


@pytest.mark.parametrize("link", Evaluation.links)
def test_link_input(browse, link):
    """Function to test link input validation in form."""
    evaluation_page = setup_for_test(browse)
    evaluation_page.click_select_user()
    evaluation_page.selected_usered()
    evaluation_page.select_evaluation_quartur()
    evaluation_page.select_quartur()
    evaluation_page.input_score_value(Evaluation.random_score_value)
    evaluation_page.select_evaluation_quartur()
    evaluation_page.input_evaluation_link(link)
    submit_button = evaluation_page.get_submit_button()
    if validators.url(link):
        assert submit_button.is_enabled()
    else:
        assert not submit_button.is_enabled()


@pytest.mark.parametrize("number", Evaluation.numbers)
def test_score_number_input(browse, number):
    """Function to test link input validation in form."""
    evaluation_page = setup_for_test(browse)
    evaluation_page.click_select_user()
    evaluation_page.selected_usered()
    evaluation_page.select_evaluation_quartur()
    evaluation_page.select_quartur()
    evaluation_page.select_evaluation_quartur()
    evaluation_page.input_evaluation_link("https://www.example.com")
    evaluation_page.input_score_value(number)
    submit_button = evaluation_page.get_submit_button()
    if str.isdigit(number):
        assert submit_button.is_enabled()
    else:
        assert not submit_button.is_enabled()
