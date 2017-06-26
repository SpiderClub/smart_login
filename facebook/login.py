import requests
from selenium import webdriver
from bs4 import BeautifulSoup

session = requests.Session()

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/58.0.3029.110 Safari/537.36'
}

proxies = {
    'http': 'socks5://127.0.0.1:1086',
    'https': 'socks5://127.0.0.1:1086'
}


def get_args(html):
    soup = BeautifulSoup(html, 'html.parser')
    first_form = soup.find(attrs={'id': 'login_form'})
    lsd = first_form.find(attrs={'name': 'lsd'}).get('value', '')
    lgndim = first_form.find(attrs={'name': 'lgndim'}).get('value', '')
    lgnrnd = first_form.find(attrs={'name': 'lgnrnd'}).get('value', '')
    lgnjs = first_form.find(attrs={'name': 'lgnjs'}).get('value', '')
    timezone = first_form.find(attrs={'name': 'timezone'}).get('value')
    locale = 'zh_CN'
    login_source = 'login_bluebar'
    return dict(
        lsd=lsd,
        lgndim=lgndim,
        lgnjs=lgnjs,
        lgnrnd=lgnrnd,
        timezone=timezone,
        locale=locale,
        login_source=login_source,
    )


def pre_login(url):
    resp = session.get(url, headers=headers)
    if resp.status_code != 200:
        raise Exception('login page request error')
    return resp.text


def login(name, passwd, url, data):
    data.update({'email': name, 'pass': passwd})
    session.post(url, data, headers)


if __name__ == '__main__':
    login_name = input('input your account\n')
    login_pass = input('input your password\n')

    first_url = 'https://www.facebook.com/'
    page_source = pre_login(first_url)
    post_url = 'https://www.facebook.com/login.php?login_attempt=1&lwv=111'
    args = get_args(page_source)

    login(login_name, login_pass, post_url, args)

    check_url = 'https://www.facebook.com/profile.php?id=100017638279480&hc_ref=NEWSFEED&fref=nf'
    resp = session.get(url=check_url, headers=headers)
    print(resp.text)
