from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
browser = webdriver.Chrome()
name = "17863108601"
pwd = "135792468shu"

def process_cookies(cookies):
    dict = {}
    for cookie in cookies:
        dict[cookie['name']] = cookie['value']
    return dict

#模拟用户登陆并记录cookie
if __name__ == "__main__":
    browser.implicitly_wait(10)
    browser.get('https://accounts.douban.com/passport/login')

    use_pwd_btn = browser.find_element(By.XPATH, '//li[@class="account-tab-account"]')
    use_pwd_btn.click()

    name_input = browser.find_element(By.ID, 'username')
    name_input.send_keys(name)

    pwd_input = browser.find_element(By.ID, 'password')
    pwd_input.send_keys(pwd)

    login_btn = browser.find_element(By.XPATH, '//a[@class="btn btn-account btn-active"]')
    login_btn.click()

    cookies = browser.get_cookies()
    # 只包含name和value
    cookies = process_cookies(cookies)
    print(cookies)
    time.sleep(5)
    # with open('cookies_error.json', 'w') as f:
    #     json.dump(cookies, f)
    # browser.close()
    cookies = browser.get_cookies()
    # 只包含name和value
    cookies = process_cookies(cookies)
    print(cookies)
