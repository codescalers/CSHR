"""page objects."""
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Login:
    """login class."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')

    def __init__(self, browser):
        self.browser = browser

    def enter_email(self, email):
        email_input = self.browser.find_element(*self.email)
        email_input.clear()
        email_input.send_keys(email)

    def enter_password(self, password):
        password_input = self.browser.find_element(*self.password)
        password_input.clear()
        password_input.send_keys(password)

    def click_login_button(self):
        return self.browser.find_element(*self.login_button)


class Vacation:
    """Vacation class."""
    dashboard_button = (By.XPATH, "//a[contains(@href, '/dashboard')]")
    xpath_for_section = '/html/body/div[20]/div[2]/section/div/div[2]/div/'
    random_userx2 = 'div[2]/div/div/div/div/div/div/div/ul/li[3]/div/div/div'
    random_user = (By.XPATH, xpath_for_section + random_userx2)
    random_user_namex1 = '//*[@id="v-tabs-user-vacation-balance"]/div/div/'
    random_user_namex2 = 'div/div[1]/div/div/div/div[1]/button'
    users_button = (By.XPATH, random_user_namex1 + 'div/div/div/div/div')
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

    def __init__(self, browser):
        self.browser = browser

    def click_dashboard_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.dashboard_button))
        dashboard_button = self.browser.find_element(*self.dashboard_button)
        dashboard_button.click()

    def click_users_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.users_button))
        users_button = self.browser.find_element(*self.users_button)
        users_button.click()

    def click_random_user(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.random_user))
        random_user = self.browser.find_element(*self.random_user)
        random_user.click()

    def click_load_balance_button(self):
        load_balanc_button = self.browser.find_element(*self.load_balanc_butt)
        load_balanc_button.click()

    def enter_leave_execuses(self, leave_number):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.leave_execuses))
        leave_execuses = self.browser.find_element(*self.leave_execuses)
        leave_execuses.click()
        leave_execuses.send_keys(leave_number)

    def enter_annual_leaves(self, annual_number):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.annual_leaves))
        annual_leaves = self.browser.find_element(*self.annual_leaves)
        annual_leaves.click()
        annual_leaves.send_keys(annual_number)

    def enter_emergency_leaves(self, emergency_number):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.emergency_leaves))
        emergency_leaves = self.browser.find_element(*self.emergency_leaves)
        emergency_leaves.click()
        emergency_leaves.send_keys(emergency_number)

    def click_delete_old_balance_button(self):
        button = self.browser.find_element(*self.delete_old_balance_button)
        button.click()

    def click_submit_button(self):
        submit_button = self.browser.find_element(*self.submit_button)
        submit_button.click()

    def get_random_user_name(self):
        return self.browser.find_element(*Vacation.random_user_name)

    def get_load_balanc_button(self):
        return self.browser.find_element(*Vacation.load_balanc_butt)

    def get_user_after_selected(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.user_name_selected))
        return self.browser.find_element(*Vacation.user_name_selected)

    def get_annual_error_message(self):
        return self.browser.find_element(*Vacation.annual_error_message)

    def get_leave_error_message(self):
        return self.browser.find_element(*Vacation.leave_error_message)

    def get_emergency_error_message(self):
        return self.browser.find_element(*Vacation.emergency_error_message)

    def get_annual_leaves(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.annual_leaves))
        return self.browser.find_element(*Vacation.annual_leaves)

    def get_leave_execuses(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.leave_execuses))
        return self.browser.find_element(*Vacation.leave_execuses)

    def get_emergency_leaves(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.emergency_leaves))
        return self.browser.find_element(*Vacation.emergency_leaves)

    def get_submit_button(self):
        return self.browser.find_element(*Vacation.submit_button)


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
    emergency_leave_text = (By.XPATH, profile_text + emergency_leaves_text1)

    def __init__(self, browser):
        self.browser = browser

    def click_employees_button(self):
        employees_button = self.browser.find_element(*self.employees_button)
        employees_button.click()

    def click_random_profile(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.random_profile))
        random_profile = self.browser.find_element(*self.random_profile)
        random_profile.click()

    def get_annual_leaves_text(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.annual_leaves_text))
        annual_text = self.browser.find_element(*self.annual_leaves_text)
        return annual_text.text

    def get_emergency_leaves_text(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.emergency_leave_text))
        emergency_text = self.browser.find_element(*self.emergency_leave_text)
        return emergency_text.text

    def get_leave_execus_text(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.leave_execus_text))
        leave_text = self.browser.find_element(*self.leave_execus_text)
        return leave_text.text
