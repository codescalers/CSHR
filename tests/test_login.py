import time
from pages.meeting import login ,meeting
import pytest
from selenium import webdriver
from utils.Base import base_url
@pytest.fixture
def driver1():
    driver = webdriver.Chrome()
    driver.get(base_url)
    yield driver
    driver.quit()
def to_login(driver1):
    email_input = driver1.find_element(*login.email)
    email_input.send_keys("A@test.cs")
    password_input = driver1.find_element(*login.password)
    password_input.send_keys("123456789")
    login_button = driver1.find_element(*login.login_button)
    login_button.click()
    time.sleep(3)
def test_Creation_Meeting(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    # Write start date
    Start_Date = driver1.find_element(*meeting.Start_Date)
    Start_Date.clear()
    Start_Date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*meeting.selected_people)
    selected_people.click()
    # Enter the meeting location
    location = driver1.find_element(*meeting.location)
    location.send_keys("online")
    # Click the fill button
    fill_button = driver1.find_element(*meeting.fill_button)
    try:fill_button.click()
    except ImportError:
        assert True 
    # Enter the meeting link
    Link = driver1.find_element(*meeting.Link)
    Link.send_keys("www.com")
    # Configure the meeting time input
    meeting_time = driver1.find_element(*meeting.meeting_time)
    driver1.execute_script("arguments[0].setAttribute('autocomplete', 'off')",meeting_time)
    meeting_time.clear()
    meeting_time.send_keys("12:30PM")
    # Click the submit button
    submit_button = driver1.find_element(*meeting.submit_button)
    try:submit_button.click()
    except ImportError:
        assert True
def test_Selection_Date_from_Calendar(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    #Select day from calendar
    random_day=driver1.find_element(*meeting.random_day)
    random_day.click()
    Start_Date = driver1.find_element(*meeting.Start_Date)
    input_value = Start_Date.get_attribute("value")
    assert input_value == "2023-08-25"
@pytest.mark.parametrize("invalid_dates", ["2023-08-99", "33333-08-12", "2023-88-99", "0000-00-00"])
def test_Date_Format_validation(driver1,invalid_dates):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    # Write invalid start date
    Start_Date = driver1.find_element(*meeting.Start_Date)
    Start_Date.clear()
    Start_Date.send_keys(invalid_dates)
    time.sleep(3)
    date_error_message = driver1.find_element(*meeting.date_error_message)
    assert "Success!" != date_error_message.text
def test_Missing_Attendee(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    # Write start date
    Start_Date = driver1.find_element(*meeting.Start_Date)
    Start_Date.clear()
    Start_Date.send_keys("2023-08-24")
    # Enter the meeting location
    location = driver1.find_element(*meeting.location)
    location.send_keys("online")
    # Click the fill button
    fill_button = driver1.find_element(*meeting.fill_button)
    assert  not fill_button.is_enabled()
def test_Missing_location(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    # Write start date
    Start_Date = driver1.find_element(*meeting.Start_Date)
    Start_Date.clear()
    Start_Date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*meeting.selected_people)
    selected_people.click()
    # Click the fill button
    fill_button = driver1.find_element(*meeting.fill_button)
    assert  not fill_button.is_enabled()
def test_remove_someone_in_people(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    # Write start date
    Start_Date = driver1.find_element(*meeting.Start_Date)
    Start_Date.clear()
    Start_Date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*meeting.selected_people)
    selected_people.click()
    # Enter the meeting location
    location = driver1.find_element(*meeting.location)
    location.send_keys("online")
    # Click the fill button
    fill_button = driver1.find_element(*meeting.fill_button)
    assert  fill_button.is_enabled()
    delete_people_button = driver1.find_element(*meeting.delete_people_button)
    delete_people_button.click()
    assert not fill_button.is_enabled()
def test_Missing_Meeting_Link(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    # Write start date
    Start_Date = driver1.find_element(*meeting.Start_Date)
    Start_Date.clear()
    Start_Date.send_keys("2023-08-24")
    # Click on the  people combo box
    combo_box = driver1.find_element(*meeting.combo_box)
    combo_box.click()
    # select people
    selected_people = driver1.find_element(*meeting.selected_people)
    selected_people.click()
    # Enter the meeting location
    location = driver1.find_element(*meeting.location)
    location.send_keys("online")
    time.sleep(2)
    # Click the fill button
    fill_button = driver1.find_element(*meeting.fill_button)
    fill_button.click()
    # Configure the meeting time input
    meeting_time = driver1.find_element(*meeting.meeting_time)
    driver1.execute_script("arguments[0].setAttribute('autocomplete', 'off')",meeting_time)
    meeting_time.clear()
    meeting_time.send_keys("12:30PM")
     # Click the submit button
    submit_button = driver1.find_element(*meeting.submit_button)
    assert not submit_button.is_enabled()
def test_Meeting_Link_validation(driver1):
    to_login(driver1)
    # Click on the meeting button
    meeting_button=driver1.find_element(*meeting.meeting_button)
    meeting_button.click()
    time.sleep(2)
    Link_error_message = driver1.find_element(*meeting.Link_error_message)
    assert "Meeting Link is invalid" == Link_error_message.text
    