# -*- coding:utf-8 -*-
# python-version: 3.51

import requests
from bs4 import BeautifulSoup

# 知乎登陆的时候并没有在前台做过多的加密，只是每次捕捉了它的xsrf就行了，和csdn的模拟登陆一样
session = requests.session()

#要提交的参数
headers =  {
                "User_Agent":"Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.75 Safari/537.36",
                "refer":"http://www.zhihu.com/"
            }

#从原始界面拿到 _xsrf,第一次post
get_url = 'http://www.zhihu.com/#signin'

phone_num = '****'
password = '****'
remember_me = 'true'


xsrf_url =  session.get(get_url,headers=headers).text
soup_one = BeautifulSoup(xsrf_url,'html.parser')
xsrf = soup_one.body.find('div',{'class':'index-main'}).find('div',{'class':'index-main-body'}).form.find('input',{'name':'_xsrf'}).attrs['value']

post_data1 = {
                'phone_num': phone_num,
                'password': password,
                'remember_me': remember_me,
                 '_xsrf': xsrf
              }

r = session.post('http://www.zhihu.com/login/phone_num', data=post_data1, headers=headers)

if r.status_code == 200:
    print('模拟登陆成功')
else:
    print('模拟登陆失败')





