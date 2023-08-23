"""page objects."""
from selenium.webdriver.common.by import By


class Login:
    """login class."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')


class Meeting:
    """Meeting class."""
    xpath_part1 = '//*[@id="isloading"]/div[2]'
    xpath_part2 = '/div[1]/div/button[2]'
    meeting_button = (By.XPATH, xpath_part1 + xpath_part2)
    Start_Date = (By.XPATH, '//input[@placeholder="Start Date"]')
    xpath_partcomb1 = '//div[@class="select-container'
    xpath_partcomb2 = ' my-2 svelte-1v9yc5w"]'
    combo_box = (By.XPATH, xpath_partcomb1+xpath_partcomb2)
    xpath_part3 = '//*[@id="isloading"]/div[2]/div[2]/div[2]/form/div[1]'
    xpath_part4 = '/div/div/ul/li[2]/div/div/div/span'
    selected_people = (By.XPATH, xpath_part3 + xpath_part4)
    location = (By.XPATH, '//input[@placeholder="Meeting Location"]')
    xpath_part5 = '//*[@id="isloading"]/div[2]/div[2]'
    xpath_part6 = '/div[2]/form/div[3]/button'
    fill_button = (By.XPATH, xpath_part5 + xpath_part6)
    Link = (By.XPATH, '//input[@placeholder="Meeting Link"]')
    meeting_time = (By.XPATH, '//input[@type="time"]')
    submit_button = (By.XPATH, '//*[@type="submit"]')
    random_day = (By.XPATH, '//*[@id="highlight"]/table/tr[5]/td[6]')
    xpath_part7 = '/html/body/div[4]/div[2]/div/div/div/div[1]/div[2]'
    xpath_part8 = '/div/fieldset/div[2]/div[2]/div[1]/div/div[1]/span'
    date_error_message = (By.XPATH, xpath_part7 + xpath_part8)
    xpath_part9 = '//*[@id="isloading"]/div[2]/div[2]/div[2]'
    xpath_part10 = '/form/div[1]/div/div/div[1]/button'
    delete_people_button = (By.XPATH, xpath_part9 + xpath_part10)
    xpath_part11 = '/html/body/div[4]/div[2]/div/div/div/'
    xpath_part12 = 'div[1]/div[2]/div/fieldset/div[2]/div[2]/div[2]'
    xpath_part13 = '/div/div/div/div[2]/form/div[1]/div/div[1]/span'
    Link_error_message = (By.XPATH, xpath_part11 + xpath_part12 + xpath_part13)
