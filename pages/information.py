"""page objects."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class lnformation:
    """information class."""
    settings_button = (By.XPATH, "//a[@href='/settings']")
    add_informtion = (By.XPATH, '')
    add_new_skill = (By.XPATH, '//*[@id="custom-id"]')
    confirm_xpath = '//*[@id="ex2-tabs-3"]/div/div/div/div[1]/div[2]'
    confirm_button = (By.XPATH, confirm_xpath+'/div')
    section_path = '/html/body/div[22]/div[2]/section/div/div[2]/div[3]/div/'
    submit_button = (By.XPATH, section_path+'div/div/div[1]/div[2]/div/button')
    elemnts_xpath = '/html/body/div[10]/div[2]/section/div/div/div[2]/div[2]/'
    elements = (By.XPATH, elemnts_xpath+'div[1]/div/div[2]')
    profile = (By.XPATH, '//*[@id="header"]/div/div/div[2]/a')
    skill_add_xpath = '/div/div/div[1]/div[2]/div/div/div/div[2]'
    skill_add_message = (By.XPATH, section_path+skill_add_xpath)
    delete_skill_xpath = 'div/div/div[1]/div[1]/div/div[2]/div/span/span'
    delete_skill = (By.XPATH, section_path+delete_skill_xpath)
    course_name = (By.XPATH, "//input[@placeholder='Enter course name']")
    course_link = (By.XPATH, "//input[@placeholder='Enter course link']")

    def __init__(self, browser):
        self.browser = browser

    def click_settings_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.settings_button))
        dash_button = self.browser.find_element(*lnformation.settings_button)
        dash_button.click()

    def click_add_informtion(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.add_informtion))
        add_button = self.browser.find_element(*lnformation.add_informtion)
        add_button.click()

    def input_add_new_skill(self, link):
        add_skill = self.browser.find_element(*lnformation.add_new_skill)
        add_skill.send_keys(link)

    def click_confirm_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.confirm_button))
        confirm_button = self.browser.find_element(*lnformation.confirm_button)
        confirm_button.click()

    def click_add_skill_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.confirm_button))
        submit = self.browser.find_element(*lnformation.confirm_button)
        submit.click()

    def click_submit_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.submit_button))
        submit = self.browser.find_element(*lnformation.submit_button)
        submit.click()

    def click_profile_icon(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.profile))
        profile = self.browser.find_element(*lnformation.profile)
        profile.click()

    def get_elements(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.elements))
        return self.browser.find_element(*lnformation.elements)

    def get_p_elements(self):
        return lnformation.get_elements(self).find_elements(By.TAG_NAME, 'p')

    def get_skill_add_message(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.skill_add_message))
        return self.browser.find_element(*lnformation.skill_add_message)

    def click_delete_skill_in_tuble(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.delete_skill))
        delete_skill = self.browser.find_element(*lnformation.delete_skill)
        delete_skill.click()

    def input_course_name(self, course_name):
        name = self.browser.find_element(*lnformation.course_name)
        name.send_keys(course_name)

    def input_course_link(self, course_link):
        link = self.browser.find_element(*lnformation.course_link)
        link.send_keys(course_link)
