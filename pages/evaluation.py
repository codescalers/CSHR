"""page objects."""
import random
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.utils import create_links, create_numbers


class Evaluation:
    """Evaluation class."""
    dashboard_button = (By.XPATH, "//a[contains(@href, '/dashboard')]")
    eval_path = '//*[@id="v-tabs-user-eval"]/div/div/div/form/div/'
    select_user = (By.XPATH, eval_path+'div[1]/div/div/div')
    selected_userx = eval_path+'div[1]/div/div/div/ul/li[3]/div/div/div'
    selected_user = (By.XPATH, selected_userx)
    name_befor = (By.XPATH, selected_userx+'/span')
    user_name_after_selectedx = eval_path+'div[1]/div/div/div/div[1]/button'
    user_name_after_selected = (By.XPATH,  user_name_after_selectedx)
    evaluation_quartur_xpath = eval_path+'div[2]/div/div/div'
    evaluation_quartur = (By.XPATH, evaluation_quartur_xpath)
    quartur_name_befor = (By.XPATH, evaluation_quartur_xpath + '/div')
    quartur_name_after = (By.XPATH, evaluation_quartur_xpath+'/div[1]/button')
    selected_quartur = (By.XPATH, eval_path+'div[2]/div/div/div/ul/li[3]/div')
    link_path1 = '/html/body/div[20]/div[2]/section/div/div[2]/div/div[4]/div'
    link_path2 = '/div/div/form/div/div[3]/div/div/input'
    evaluation_link = (By.XPATH, link_path1+link_path2)
    score_value = (By.XPATH, '//input[@placeholder="Enter score value"]')
    random_score_value = random.randint(1, 1000)
    submit_button = (By.XPATH, link_path1+'/div/div/form/div/div[5]/button')
    links = create_links(5)
    numbers = create_numbers(5)

    def __init__(self, browser):
        self.browser = browser

    def click_dashboard_button(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.dashboard_button))
        dash_button = self.browser.find_element(*Evaluation.dashboard_button)
        dash_button.click()

    def click_select_user(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.select_user))
        select_user = self.browser.find_element(*Evaluation.select_user)
        select_user.click()

    def selected_usered(self):
        wait = WebDriverWait(self.browser, 30)
        wait.until(EC.visibility_of_element_located(self.selected_user))
        select_usered = self.browser.find_element(*Evaluation.selected_user)
        select_usered.click()

    def select_evaluation_quartur(self):
        eval_qurtur = self.browser.find_element(*Evaluation.evaluation_quartur)
        eval_qurtur.click()

    def select_quartur(self):
        selec_quartur = self.browser.find_element(*Evaluation.selected_quartur)
        selec_quartur.click()

    def input_evaluation_link(self, link):
        eval_link = self.browser.find_element(*Evaluation.evaluation_link)
        eval_link.send_keys(link)

    def input_score_value(self, value):
        score_value = self.browser.find_element(*Evaluation.score_value)
        score_value.clear()
        score_value.send_keys(value)

    def get_submit_button(self):
        return self.browser.find_element(*Evaluation.submit_button)

    def get_name_befor(self):
        return self.browser.find_element(*Evaluation.name_befor)

    def get_user_name_after_selected(self):
        return self.browser.find_element(*Evaluation.user_name_after_selected)

    def get_quartur_name_befor(self):
        return self.browser.find_element(*Evaluation.quartur_name_befor)

    def get_quartur_name_after(self):
        return self.browser.find_element(*Evaluation.quartur_name_after)
