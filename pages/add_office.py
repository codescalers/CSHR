"""page objects."""
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


class Office:
    """Office class."""
    dashboard_button = (By.XPATH, "//a[contains(@href, '/dashboard')]")
    office_name = (By.XPATH, '//input[@placeholder="Office name."]')
    office_country = (By.XPATH, '//input[@placeholder="office country"]')
    weekend_x = '//*[@id="v-tabs-office"]/div/div/div/form/div[3]/div/div/div'
    weekend_holidays = (By.XPATH, weekend_x)
    selected_weekend_holiday = (By.XPATH, weekend_x + '/ul/li[3]')
    submit_xpath = '/html/body/div[20]/div[2]/section/div/div[2]/div/div[6]'
    submit_button = (By.XPATH, submit_xpath+'/div/div/div/form/div[4]/button')
    selected_holiday_name = (By.XPATH, weekend_x + '/ul/li[3]/div/div')
    holiday_name_button = (By.XPATH, weekend_x + '/div[1]/button')

    def __init__(self, browser):
        self.browser = browser

    def click_dashboard_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.dashboard_button))
        dashboard_button = self.browser.find_element(*self.dashboard_button)
        dashboard_button.click()

    def click_weekend_holidays(self):
        self.browser.find_element(*Office.weekend_holidays).click()

    def get_selected_holiday_name(self):
        return self.browser.find_element(*Office.selected_holiday_name)

    def click_selected_weekend_holiday(self):
        self.browser.find_element(*Office.selected_weekend_holiday).click()

    def get_holiday_name_button(self):
        return self.browser.find_element(*Office.holiday_name_button)

    def get_office_name(self):
        return self.browser.find_element(*Office.office_name)

    def get_office_country(self):
        return self.browser.find_element(*Office.office_country)

    def get_submit_button(self):
        return self.browser.find_element(*Office.submit_button)

    def enter_office_name(self, name):
        office_name = self.get_office_name()
        office_name.click()
        office_name.send_keys(name)

    def enter_office_country(self, country):
        office_country = self.get_office_country()
        office_country.click()
        office_country.send_keys(country)
