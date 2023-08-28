"""page objects."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import generate_random_emails, generate_random_passwords
from utils.utils import get_random_invalid_email


class Login:
    """class Login."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    xpath_profile = '//span[@class="user-profile-image rounded-circle svelte-1'
    profile = (By.XPATH, xpath_profile + '8t1c4h" and contains(text(), "AW")]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')
    passwords = generate_random_passwords(2)
    emails = generate_random_emails(2)
    invalid_emails = get_random_invalid_email(2)

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

    def get_profile(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.profile))
        return self.browser.find_element(*self.profile)

    def get_undefined_message(self):
        return self.browser.find_element(*self.undefined_message)
