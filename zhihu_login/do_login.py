#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'zkqiang'
__zhihu__ = 'https://www.zhihu.com/people/z-kqiang'
__github__ = 'https://github.com/zkqiang/Zhihu-Login'

import requests
import time
import re
import base64
import hmac
import hashlib
import json
import matplotlib.pyplot as plt
from http import cookiejar
from PIL import Image

HEADERS = {
    'Connection': 'keep-alive',
    'Host': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com/',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36'
    }
LOGIN_URL = 'https://www.zhihu.com/signup'
LOGIN_API = 'https://www.zhihu.com/api/v3/oauth/sign_in'
FORM_DATA = {
    'client_id': 'c3cef7c66a1843f8b3a9e6a1e3160e20',
    'grant_type': 'password',
    'source': 'com.zhihu.web',
    # 可将登录手机号和密码填在这里
    'username': '',
    'password': '',
    'lang': 'cn',
    'ref_source': 'homepage'
}


class ZhihuAccount(object):

    def __init__(self):
        self.login_url = LOGIN_URL
        self.login_api = LOGIN_API
        self.login_data = FORM_DATA.copy()
        self.session = requests.session()
        self.session.headers = HEADERS.copy()
        self.session.cookies = cookiejar.LWPCookieJar(filename='./cookies.txt')

    def login(self, load_cookies=True):
        """
        模拟登录知乎
        :param load_cookies: 是否读取上次保存的 Cookies
        :return: bool
        """
        if load_cookies and self.load_cookies():
            if self.check_login():
                print('已读取 Cookies 并登录成功')
                return True
            else:
                print('保存的 Cookies 已过期，将重新登录')

        headers = self.session.headers.copy()
        headers.update({
            'authorization': 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20',
            'X-Xsrftoken': self._get_token()
        })
        self.login_data.update({
            'username': self._input_data('username', '登录手机'),
            'password': self._input_data('password', '密码')
        })
        timestamp = str(int(time.time()*1000))
        self.login_data.update({
            'captcha': self._get_captcha(headers),
            'timestamp': timestamp,
            'signature': self._get_signature(timestamp)
        })

        resp = self.session.post(self.login_api, data=self.login_data, headers=headers)
        print(resp.text)
        if '验证码' in resp.text:
            print('验证码错误')
        elif self.check_login():
            print('登录成功')
            return True
        print('登录失败')
        return False

    def load_cookies(self):
        """
        读取 Cookies 文件加载到 Session
        :return: bool
        """
        try:
            self.session.cookies.load(ignore_discard=True)
            return True
        except FileNotFoundError:
            print('Cookies.txt 未找到，读取失败')
        return False

    def check_login(self):
        """
        检查登录状态，访问登录页面出现跳转则是已登录，
        如登录成功保存当前 Cookies
        :return: bool
        """
        resp = self.session.get(self.login_url, allow_redirects=False)
        if resp.status_code == 302:
            self.session.cookies.save()
            return True
        return False

    def _get_token(self):
        """
        从登录页面获取 token
        :return:
        """
        resp = self.session.get(self.login_url)
        token = re.findall(r'_xsrf=([\w|-]+)', resp.headers.get('Set-Cookie'))[0]
        return token

    def _get_captcha(self, headers, lang='cn'):
        """
        请求验证码的 API 接口，无论是否需要验证码都需要请求一次
        如果需要验证码会返回图片的 base64 编码
        可选择两种验证码，需要人工输入
        :param headers: 带授权信息的请求头部
        :param lang: 验证码的种类，中文是选倒立汉字，英文是输入字符
        :return: 验证码的 POST 参数
        """
        if lang == 'cn':
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=cn'
        else:
            api = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
        resp = self.session.get(api, headers=headers)
        show_captcha = re.search(r'true', resp.text)
        if show_captcha:
            put_resp = self.session.put(api, headers=headers)
            img_base64 = re.findall(
                r'"img_base64":"(.+)"', put_resp.text, re.S)[0].replace(r'\n', '')
            with open('./captcha.jpg', 'wb') as f:
                f.write(base64.b64decode(img_base64))
            img = Image.open('./captcha.jpg')
            if lang == 'cn':
                plt.imshow(img)
                print('点击所有倒立的汉字，按回车提交')
                points = plt.ginput(7)
                capt = json.dumps({'img_size': [200, 44],
                                   'input_points': [[i[0]/2, i[1]/2] for i in points]})
            else:
                img.show()
                capt = input('请输入图片里的验证码：')
            # 这里必须先把参数 POST 验证码接口
            self.session.post(api, data={'input_text': capt}, headers=headers)
            return capt
        return ''

    def _get_signature(self, timestamp):
        """
        通过 Hmac 算法计算返回签名
        实际是几个固定字符串加时间戳
        :param timestamp: 时间戳
        :return: 签名
        """
        ha = hmac.new(b'd1b964811afb40118a12068ff74a12f4', digestmod=hashlib.sha1)
        grant_type = self.login_data['grant_type']
        client_id = self.login_data['client_id']
        source = self.login_data['source']
        ha.update(bytes((grant_type + client_id + source + timestamp), 'utf-8'))
        return ha.hexdigest()

    def _input_data(self, key, data_name):
        """
        用于手动输入指定 form_data 参数
        :param key: 键名
        :param data_name: 用于输入提示中文名
        :return: 输入的值
        """
        value = self.login_data.get(key)
        if not value:
            value = input('请输入{}：'.format(data_name))
        return value


if __name__ == '__main__':
    account = ZhihuAccount()
    account.login()
