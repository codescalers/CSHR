"""page objects."""
from selenium.webdriver.common.by import By


class Login:
    """login class."""
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')


class Employees:
    """Employees class."""
    xpath1 = "//*[name()='svg' and contains(@class, 'bi-microsoft-teams')]"
    employees_button = (By.XPATH, xpath1)
    parent_element = (By.CLASS_NAME, "row.justify-content-between")
    profile_links = (By.TAG_NAME, "a")
    profile_text_element = (By.CLASS_NAME, "user-profile-image")
    profile_names = ["AD", "MR", "AW", "TB"]
    xpath_random_profile1 = '//*[@id="body-pd"]/div[2]/div/div/div'
    xpath_random_profile2 = '/div/div/div[1]/a/div/p'
    random_profile = (By.XPATH, xpath_random_profile1+xpath_random_profile2)
    xpath_email_profile1 = '//*[@id="body-pd"]/div[2]/section/div/div'
    xpath_email_profile2 = '/div[2]/div[1]/div/div[2]/div[2]/p'
    email_profile = (By.XPATH, xpath_email_profile1+xpath_email_profile2)
    xpath_my_profile1 = '//*[@id="body-pd"]/div[2]/div/div/div/div/div/div[3]'
    my_profile = (By.XPATH, xpath_my_profile1 + '/a/div')
    xpath_pr_email = '//*[@id="body-pd"]/div[2]/section/div/div/div[2]/div[1]'
    my_profile_email = (By.XPATH, xpath_pr_email + '/div/div[2]/div[2]/p')
