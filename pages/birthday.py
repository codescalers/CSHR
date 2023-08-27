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


class Birthday:
    """Birthday class."""
    text1 = "//section[@class='task task--primary svelte-11utwz3']"
    text2 = '//button'
    birthday_button = (By.XPATH, text1+text2)

    def __init__(self, browser):
        self.browser = browser

    def get_birthday_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.birthday_button))
        return self.browser.find_element(*self.birthday_button)
