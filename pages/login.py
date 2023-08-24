from selenium.webdriver.common.by import By


class login:
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    xpath_profile = '//span[@class="user-profile-image rounded-circle svelte-1'
    profile = (By.XPATH, xpath_profile + '8t1c4h" and contains(text(), "AW")]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')
