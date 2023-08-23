from selenium.webdriver.common.by import By

class login:
    email = (By.XPATH, '//*[@type="email"]')
    password = (By.XPATH, '//*[@type="password"]')
    login_button = (By.XPATH, '//button[text()="Login"]')
    profile = (By.XPATH, '//span[@class="user-profile-image rounded-circle svelte-18t1c4h" and contains(text(), "AW")]')
    undefined_message = (By.XPATH, '//*[@id="liveToast"]/div[2]')
class meeting:
    meeting_button=(By.XPATH,'//*[@id="isloading"]/div[2]/div[1]/div/button[2]')
    Start_Date = (By.XPATH,'//input[@placeholder="Start Date"]')
    combo_box = (By.XPATH, '//div[@class="select-container my-2 svelte-1v9yc5w"]')
    selected_people = (By.XPATH, '//*[@id="isloading"]/div[2]/div[2]/div[2]/form/div[1]/div/div/ul/li[2]/div/div/div/span')
    location = (By.XPATH,'//input[@placeholder="Meeting Location"]')
    fill_button = (By.XPATH,'//*[@id="isloading"]/div[2]/div[2]/div[2]/form/div[3]/button')
    Link = (By.XPATH,'//input[@placeholder="Meeting Link"]')
    meeting_time = (By.XPATH,'//input[@type="time"]')
    submit_button = (By.XPATH,'//*[@type="submit"]')
    random_day = (By.XPATH,'//*[@id="highlight"]/table/tr[5]/td[6]')
    date_error_message = (By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div[1]/div[2]/div/fieldset/div[2]/div[2]/div[1]/div/div[1]/span')
    delete_people_button = (By.XPATH,'//*[@id="isloading"]/div[2]/div[2]/div[2]/form/div[1]/div/div/div[1]/button')
    Link_error_message  =(By.XPATH,'/html/body/div[4]/div[2]/div/div/div/div[1]/div[2]/div/fieldset/div[2]/div[2]/div[2]/div/div/div/div[2]/form/div[1]/div/div[1]/span')