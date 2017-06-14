# tested on ubuntu15.04
import time
from selenium import webdriver


def login(login_url, login_name, login_passwd):
    driver = webdriver.Chrome()
    driver.get(login_url)
    time.sleep(5)

    login_tab_right = driver.find_element_by_class_name('login-tab-r')
    login_tab_right.click()

    account = driver.find_element_by_id('loginname')
    password = driver.find_element_by_id('nloginpwd')
    submit = driver.find_element_by_id('loginsubmit')

    account.clear()
    password.clear()
    account.send_keys(login_name)
    password.send_keys(login_passwd)

    submit.click()
    time.sleep(5)

    jd_cookies = driver.get_cookies()
    driver.close()
    return jd_cookies

if __name__ == '__main__':
    url = 'https://passport.jd.com/new/login.aspx'
    name = input('请输入用户名:\n')
    password = input('请输入密码:\n')
    cookies = login(url, name, password)
    print(cookies)