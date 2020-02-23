import time
from secret import email, password, crush
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Instabot:

    def __init__(self):
        self.height = '208'  # default seen all story value
        self.counter = 0
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-gpu")
        self.driver = webdriver.Chrome(executable_path=ChromeDriverManager()
                                       .install(), options=chrome_options)

    def screenshoot(self):
        self.driver.save_screenshot("C:\\Users\\ASUS\\Desktop\\screenshoot\\pic{}.png".format(self.counter))
        self.counter += 1

    def login(self):
        self.driver.get('https://www.instagram.com')
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Log in with Facebook")]'))).click()
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="email"]'))).send_keys(email)
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="pass"]'))).send_keys(password)
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="loginbutton"]'))).click()

    def to_crush_page(self):
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"Not Now")]'))).click()
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//input[@placeholder="Search"]'))).send_keys(crush)
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//span[@class="Ap253" and contains(text(),crush)]'))).click()

    def check_new_story(self):
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.CLASS_NAME, 'RR-M-.h5uC0')))
        self.driver.refresh()
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.CLASS_NAME, 'RR-M-.h5uC0')))
        newheight = WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable((By.XPATH, '//canvas[@class="CfWVH"]'))).get_attribute('height')
        if self.height == newheight:
            #no new story
            print('Nothing new')
        else:
            self.driver.find_element_by_class_name('RR-M-.h5uC0').click()
            self.messenger_report()

    def messenger_report(self):
        self.driver.execute_script("window.open('');")
        self.driver.switch_to.window(self.driver.window_handles[1])
        self.driver.get("http://www.messenger.com")
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(
            (By.XPATH, '//button[@data-testid="sso_login_button"]'))).click()
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(
            (By.XPATH, '//input[@placeholder={}]'.format("'Tìm kiếm trên Messenger'")))).send_keys("Trịnh Khánh Hiệp")
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(
            (By.XPATH, '//div[contains(text(),"Người liên hệ")]/../ul/li[1]'))).click()
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(
            (By.XPATH,'//div[@aria-label="Nhập tin nhắn..."]'))).send_keys('http://www.instagram.com/stories/{}/'.format(crush))
        WebDriverWait(self.driver, 1000).until(EC.element_to_be_clickable(
            (By.XPATH, '//a[@aria-label="Gửi"]'))).click()
        self.driver.close()
        self.driver.switch_to.window(self.driver.window_handles[0])


if __name__ == '__main__':
    try:
        bot = Instabot()
        bot.login()
        bot.to_crush_page()
    except TimeoutException:
        print("Bad Internet Connection ...")
    except WebDriverException:
        print("Error Webdriver")
    while 1:
        try:
            bot.check_new_story()
            time.sleep(60)
        except TimeoutException:
            print("Bad Internet Connection ...")

    # finally:
    # bot.driver.close()
