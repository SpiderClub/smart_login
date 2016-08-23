from selenium import webdriver
import time

acount_num = input('请输入账号:')
passwd_str = input('请输入密码:')
driver = webdriver.Chrome()
url = 'http://mail.163.com/'
driver.get(url)
time.sleep(5)
# 163登陆框是使用iframe进行嵌套的，所以需要先切换到该iframe
driver.switch_to.frame('x-URS-iframe')

acount = driver.find_element_by_name('email')
acount.clear()
acount.send_keys(acount_num)

passwd = driver.find_element_by_name('password')
passwd.clear()
passwd.send_keys(passwd_str)

time.sleep(3)
click_button = driver.find_element_by_id('dologin')
click_button.click()
