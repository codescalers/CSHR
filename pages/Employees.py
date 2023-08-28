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
    my_email = "A@test.cs"

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


class Employees:
    """Employees class."""
    xpath1 = 'svg.bi.bi-microsoft-teams.nav_icon'
    employees_button = (By.CSS_SELECTOR, xpath1)
    parent_element = (By.CLASS_NAME, "row.justify-content-between")
    profile_links = (By.TAG_NAME, "a")
    profile_text_element = (By.CLASS_NAME, "user-profile-image")
    profile_names = ["AD", "MR", "AW", "TB"]
    xpath_random_profile1 = '//*[@id="body-pd"]/div[2]/div/div/div'
    xpath_random_profile2 = '/div/div/div[1]/a/div/p'
    random_profile_xpath = xpath_random_profile1+xpath_random_profile2
    random_profile = (By.XPATH, random_profile_xpath)
    random_prfile_email = (By.XPATH, random_profile_xpath + '/small[2]/cite')
    xpath_email_profile1 = '//*[@id="body-pd"]/div[2]/section/div/div'
    xpath_email_profile2 = '/div[2]/div[1]/div/div[2]/div[2]/p'
    email_profile = (By.XPATH, xpath_email_profile1+xpath_email_profile2)
    xpath_my_profile1 = '//*[@id="body-pd"]/div[2]/div/div/div/div/div/div[3]'
    my_profile = (By.XPATH, xpath_my_profile1 + '/a/div')
    xpath_pr_email = '//*[@id="body-pd"]/div[2]/section/div/div/div[2]/div[1]'
    my_profile_email = (By.XPATH, xpath_pr_email + '/div/div[2]/div[2]/p')

    def __init__(self, browser):
        self.browser = browser

    def click_dashboard_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.employees_button))
        dashboard_button = self.browser.find_element(*self.employees_button)
        dashboard_button.click()

    def get_parent_element(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.parent_element))
        return self.browser.find_element(*Employees.parent_element)

    def get_profile_links(self):
        parent_element = self.get_parent_element()
        return parent_element.find_elements(*Employees.profile_links)

    def is_profile_present(self, profile_text):
        profile_presence = {}
        for name in Employees.profile_names:
            profile_presence[name] = False

        profile_links = self.get_profile_links()
        for link in profile_links:
            profil_element = link.find_element(*Employees.profile_text_element)
            profile_text = profil_element.text
            profile_presence[profile_text] = True

        return all(value for value in profile_presence.values())

    def click_random_profile(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.random_profile))
        self.browser.find_element(*Employees.random_profile).click()

    def get_random_prfile_email(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.random_prfile_email))
        return self.browser.find_element(*Employees.random_prfile_email)

    def get_profile_email(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.email_profile))
        return self.browser.find_element(*Employees.email_profile)

    def click_my_profile(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.my_profile))
        self.browser.find_element(*Employees.my_profile).click()

    def get_my_profile_email(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.my_profile_email))
        return self.browser.find_element(*Employees.my_profile_email)
