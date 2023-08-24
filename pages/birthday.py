"""page objects."""
from selenium.webdriver.common.by import By


class Login:
    """login class."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')


class Birthday:
    """Birthday class."""
    text1 = "//section[@class='task task--primary svelte-11utwz3']"
    text2 = '//button'
    birthday_button = (By.XPATH, text1+text2)
