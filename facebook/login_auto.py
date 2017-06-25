import time
from selenium import webdriver
import requests


def sele2req_cookie(cookies):
    cookie_dict = dict()
    for cookie in cookies:
        cookie_dict[cookie['name']] = cookie['value']
    return cookie_dict

def login(url):
    name = input('input your name\n')
    passwd = input('input your password\n')
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    account = driver.find_element_by_id('email')
    password = driver.find_element_by_id('pass')
    submit = driver.find_element_by_id('loginbutton')

    account.clear()
    password.clear()
    account.send_keys(name)
    password.send_keys(passwd)

    submit.click()
    time.sleep(5)

    fb_cookies = driver.get_cookies()
    driver.close()
    return fb_cookies


if __name__ == '__main__':
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/58.0.3029.110 Safari/537.36'
    }
    proxies = {
        'http': 'socks5://127.0.0.1:1086',
        'https': 'socks5://127.0.0.1:1086'
    }
    login_url = 'https://www.facebook.com/login.php'
    cookies = login(login_url)
    req_cookies = sele2req_cookie(cookies)

    check_url = 'https://www.facebook.com/pg/loveshehebe/posts/?ref=page_internal'
    resp = requests.get(check_url, headers=headers, proxies=proxies, cookies=req_cookies)
    print(resp.text)

