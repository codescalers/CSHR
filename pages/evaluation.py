"""page objects."""
from selenium.webdriver.common.by import By


class Login:
    """login class."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')


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
