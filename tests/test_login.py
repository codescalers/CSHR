"""Module to test meeting page."""
import time
from selenium import webdriver
import pytest
from pages.meeting import Login, Meeting
from utils.Base import base_url


@pytest.fixture(name="driver1")
def driver1_fixture():
    """Function to save driver fixture."""
    driver = webdriver.Edge()
    driver.get(base_url)
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


def test_creation_meeting(driver1):
    """test for creation meeting."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    # Write start date
    start_date = driver1.find_element(*Meeting.Start_Date)
    start_date.clear()
    start_date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*Meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*Meeting.selected_people)
    selected_people.click()
    # Enter the meeting location
    location = driver1.find_element(*Meeting.location)
    location.send_keys("online")
    # Click the fill button
    fill_button = driver1.find_element(*Meeting.fill_button)
    try:
        fill_button.click()
    except ImportError:
        assert True
    # Enter the meeting linkf
    link = driver1.find_element(*Meeting.Link)
    link.send_keys("www.com")
    # Configure the meeting time input
    meeting_time = driver1.find_element(*Meeting.meeting_time)
    script = "arguments[0].setAttribute('autocomplete', 'off')"
    driver1.execute_script(script, meeting_time)
    meeting_time.clear()
    meeting_time.send_keys("12:30PM")
    # Click the submit button
    submit_button = driver1.find_element(*Meeting.submit_button)
    try:
        submit_button.click()
    except ImportError:
        assert True


def test_selection_date_from_calendar(driver1):
    """test for selection date from calendar."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    # Select day from calendar
    random_day = driver1.find_element(*Meeting.random_day)
    random_day.click()
    start_date = driver1.find_element(*Meeting.Start_Date)
    input_value = start_date.get_attribute("value")
    assert input_value == "2023-08-25"


@pytest.mark.parametrize("invalid_dates", [
    "2023-08-99",
    "33333-08-12",
    "2023-88-99",
    "0000-00-00"
])
def test_date_format_validation(driver1, invalid_dates):
    """test for date format validation with more than one date."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    # Write invalid start date
    start_date = driver1.find_element(*Meeting.Start_Date)
    start_date.clear()
    start_date.send_keys(invalid_dates)
    time.sleep(3)
    date_error_message = driver1.find_element(*Meeting.date_error_message)
    assert "Success!" != date_error_message.text


def test_missing_attendee(driver1):
    """test for missing attendee."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    # Write start date
    start_date = driver1.find_element(*Meeting.Start_Date)
    start_date.clear()
    start_date.send_keys("2023-08-24")
    # Enter the meeting location
    location = driver1.find_element(*Meeting.location)
    location.send_keys("online")
    # Click the fill button
    fill_button = driver1.find_element(*Meeting.fill_button)
    assert not fill_button.is_enabled()


def test_missing_location(driver1):
    """test for missing location."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    # Write start date
    start_date = driver1.find_element(*Meeting.Start_Date)
    start_date.clear()
    start_date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*Meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*Meeting.selected_people)
    selected_people.click()
    # Click the fill button
    fill_button = driver1.find_element(*Meeting.fill_button)
    assert not fill_button.is_enabled()


def test_remove_someone_in_people(driver1):
    """test for remove someone in people."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    # Write start date
    start_date = driver1.find_element(*Meeting.Start_Date)
    start_date.clear()
    start_date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*Meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*Meeting.selected_people)
    selected_people.click()
    # Enter the meeting location
    location = driver1.find_element(*Meeting.location)
    location.send_keys("online")
    # Click the fill button
    fill_button = driver1.find_element(*Meeting.fill_button)
    assert fill_button.is_enabled()
    delete_people_button = driver1.find_element(*Meeting.delete_people_button)
    delete_people_button.click()
    assert not fill_button.is_enabled()


def test_missing_meeting_link(driver1):
    """test for missing meeting link."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    time.sleep(4)
    # Write start date
    start_date = driver1.find_element(*Meeting.Start_Date)
    start_date.clear()
    start_date.send_keys("2023-08-25")
    time.sleep(4)
    # Click on the  people combo box
    combo_box = driver1.find_element(*Meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*Meeting.selected_people)
    selected_people.click()
    # Enter the meeting location
    location = driver1.find_element(*Meeting.location)
    location.send_keys("online")
    time.sleep(4)
    # Click the fill button
    fill_button = driver1.find_element(*Meeting.fill_button)
    fill_button.click()
    # Configure the meeting time input
    meeting_time = driver1.find_element(*Meeting.meeting_time)
    script = "arguments[0].setAttribute('autocomplete', 'off')"
    driver1.execute_script(script, meeting_time)
    meeting_time.clear()
    meeting_time.send_keys("12:30PM")
    time.sleep(4)
    # Click the submit button
    submit_button = driver1.find_element(*Meeting.submit_button)
    assert not submit_button.is_enabled()


def test_meeting_link_validation(driver1):
    """test for meeting link validation."""
    to_login(driver1)
    # Click on the meeting button
    meeting_button = driver1.find_element(*Meeting.meeting_button)
    meeting_button.click()
    time.sleep(2)
    link_error_message = driver1.find_element(*Meeting.Link_error_message)
    assert "Meeting Link is invalid" == link_error_message.text
