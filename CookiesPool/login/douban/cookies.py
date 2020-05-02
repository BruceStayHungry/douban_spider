from selenium.common.exceptions import TimeoutException
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class DoubanCookies():
    def __init__(self, username, password, browser=None):
        self.url = 'https://accounts.douban.com/passport/login'
        self.browser = browser if browser else webdriver.Chrome()
        self.wait = WebDriverWait(self.browser, 20)
        self.username = username
        self.password = password

    def open(self):
        """
        打开网页输入用户名密码并点击
        :return: None
        """
        self.browser.delete_all_cookies()
        self.browser.get(self.url)

        #切换用户名密码登陆
        use_pwd_btn = self.browser.find_element(By.XPATH, '//li[@class="account-tab-account"]')
        use_pwd_btn.click()
        #输入用户名
        name_input = self.browser.find_element(By.ID, 'username')
        name_input.send_keys(self.username)
        #输入密码
        pwd_input = self.browser.find_element(By.ID, 'password')
        pwd_input.send_keys(self.password)
        #点击登陆
        login_btn = self.browser.find_element(By.XPATH, '//a[@class="btn btn-account btn-active"]')
        time.sleep(1)
        login_btn.click()

    def password_error(self):
        """
        判断是否密码错误
        :return:
        """
        try:
            return WebDriverWait(self.browser, 5).until(
                EC.text_to_be_present_in_element((By.CLASS_NAME, "fatal-msg"), '用户名或密码错误'))
        except TimeoutException:
            return False

    def login_successfully(self):
        """
        判断是否登录成功
        :return:
        """
        try:
            return bool(
                WebDriverWait(self.browser, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'isay-links'))))
        except TimeoutException:
            return False

    def get_cookies(self):
        """
        获取Cookies
        :return:
        """
        return self.browser.get_cookies()

    def main(self):
        """
        破解入口
        :return:
        """
        self.open()
        if self.password_error():
            return {
                'status': 2,
                'content': '用户名或密码错误'
            }
        time.sleep(3)
        # 如果不需要验证码直接登录成功
        if self.login_successfully():
            cookies = self.get_cookies()
            return {
                'status': 1,
                'content': cookies
            }

if __name__ == '__main__':
    result = DoubanCookies('douban账号', 'douban密码').main()
    print(result)






