# -*-coding;utf-8 -*-

import requests
from bs4 import BeautifulSoup
# 获取登陆页面
# 提交post参数
username = input('请输入用户名')
password = input('请输入登陆密码')
session = requests.session()
header = {
    'Host': 'passport.csdn.net',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Connection': 'keep-alive',
    'Referer': 'http://www.csdn.net/'
}
login_url = 'https://passport.csdn.net/account/login?from=http://my.csdn.net/my/mycsdn'
login_page = session.get(login_url, verify=False, headers=header).text

# 提取lt, execution, _eventId
soup = BeautifulSoup(login_page, 'html.parser')

lt = soup.find(attrs={'name': 'lt'})['value']
execution = soup.find(attrs={'name': 'execution'})['value']
submit = soup.find(attrs={'name': '_eventId'})['value']

post_data = {
                'username': username,
                'password': password,
                'lt': lt,
                'execution': execution,
                '_eventId': submit
             }

session.post(login_url, data=post_data)
home_page = 'http://my.csdn.net/my/mycsdn'
r = requests.get(home_page, headers=header).text
print(r)



