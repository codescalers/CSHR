"""page objects."""
import random
from selenium.webdriver.common.by import By


class Login:
    """login class."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')


class Vacation:
    """Vacation class."""
    dashboard_button = (By.XPATH, "//a[contains(@href, '/dashboard')]")
    users_button = (By.XPATH, "//div[@class='caret svelte-1v9yc5w']")
    xpath_for_section = '/html/body/div[20]/div[2]/section/div/div[2]/div/'
    random_userx2 = 'div[2]/div/div/div/div/div/div/div/ul/li[3]/div/div/div'
    random_user = (By.XPATH, xpath_for_section + random_userx2)
    random_user_namex1 = '//*[@id="v-tabs-user-vacation-balance"]/div/div/'
    random_user_namex2 = 'div/div[1]/div/div/div/div[1]/button'
    random_user_name = (By.XPATH, random_user_namex1 + random_user_namex2)
    load_balanc_butt = (By.XPATH, "//button[contains(text(), 'Load Balance')]")
    annual_leavesx2 = 'div[2]/div/div/div/div/div[2]/div/div/input'
    annual_leaves = (By.XPATH, xpath_for_section + annual_leavesx2)
    leave_execusesx2 = 'div[2]/div/div/div/div/div[3]/div/div/input'
    leave_execuses = (By.XPATH, xpath_for_section + leave_execusesx2)
    emergency_leavesx2 = 'div[2]/div/div/div/div/div[4]/div/div/input'
    emergency_leaves = (By.XPATH, xpath_for_section + emergency_leavesx2)
    delete_old_balance_button = (By.XPATH, '//*[@id="flexCheckDefault"]')
    submit_xpath = 'div[2]/div/div/div/div/div[6]/button'
    submit_button = (By.XPATH, xpath_for_section + submit_xpath)
    user_name_selected = (By.CLASS_NAME, "user_full_name")
    error_messages = '/html/body/div[20]/div[2]/section/div/div[2]/div/div[2]/'
    annual_error = 'div/div/div/div/div[2]/div/div/div[1]/span'
    annual_error_message = (By.XPATH, error_messages+annual_error)
    leave_error = 'div/div/div/div/div[3]/div/div/div[1]/span'
    leave_error_message = (By.XPATH, error_messages+leave_error)
    emergency_error = 'div/div/div/div/div[4]/div/div/div[1]/span'
    emergency_error_message = (By.XPATH, error_messages+emergency_error)


class Employees:
    """Employees class."""
    xpath1 = "//*[name()='svg' and contains(@class, 'bi-microsoft-teams')]"
    employees_button = (By.XPATH, xpath1)
    parent_element = (By.CLASS_NAME, "row.justify-content-between")
    xpath_random_profile1 = '//*[@id="body-pd"]/div[2]/div/div/div/'
    xpath_random_profile2 = 'div/div/div[4]/a/div/h5/div[1]/a'
    random_profile = (By.XPATH, xpath_random_profile1 + xpath_random_profile2)
    xpath_email_profile1 = '//*[@id="body-pd"]/div[2]/section/div/div'
    xpath_email_profile2 = '/div[2]/div[1]/div/div[2]/div[2]/p'
    profile_text = '//*[@id="body-pd"]/div[2]/section/div/'
    annual_number = random.randint(1, 1000)
    leave_number = random.randint(1, 1000)
    emergency_number = random.randint(1, 1000)
    annual_string = f"{annual_number} / {annual_number}"
    leave_string = f"{leave_number} / {leave_number}"
    emergency_string = f"{emergency_number} / {emergency_number}"
    annual_leaves_text1 = 'div/div[2]/div[4]/div[2]/div[2]/div[1]'
    annual_leaves_text = (By.XPATH, profile_text + annual_leaves_text1)
    leave_execuses_text1 = 'div/div[2]/div[4]/div[2]/div[2]/div[3]'
    leave_execus_text = (By.XPATH, profile_text + leave_execuses_text1)
    emergency_leaves_text1 = '/div[2]/div[4]/div[2]/div[2]/div[2]'
    emergency_leaves_text = (By.XPATH, profile_text + emergency_leaves_text1)
