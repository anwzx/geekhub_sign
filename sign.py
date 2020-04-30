import re
import requests
import json
import os


session = requests.Session()
session.headers["User-Agent"] = "Mozilla/5.0 (iPhone; CPU iPhone OS 12_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/12.0 Mobile/15E148 Safari/604.1"

COOKIES_PATH = './cookies.txt'


def authenticity_token():
    """获取authenticity_token"""
    res = session.get('https://geekhub.com/users/sign_in')
    pattern = r'<form class="simple_form new_user" id="new_user" novalidate="novalidate" action="/users/sign_in" accept-charset="UTF-8" method="post"><input type="hidden" name="authenticity_token" value="(.*?)" />'
    result = re.search(pattern=pattern, string=str(res.text)).group(1)
    print(result)
    return result


def _rucaptcha():
    """获取验证码"""
    res = session.get('https://geekhub.com/rucaptcha/')
    with open('./验证码.gif', 'wb') as f:
        f.write(res.content)


def login(authenticity_token) -> requests.cookies.RequestsCookieJar:
    """登录"""
    data = {
        "authenticity_token": authenticity_token,
        "user[login]": 'xxx',  # 用户名
        "user[password]": 'xxx',  # 密码
        "_rucaptcha": input('请输入验证码(当前目录):'),
        "user[remember_me]": 'on'
    }
    url = 'https://geekhub.com/users/sign_in'
    res = session.post(url=url, data=data)
    if "退出" in res.text:
        print("登录成功")
        cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
        with open('./cookies.txt', 'w+') as f:
            json.dump(cookies_dict, f)
        return session.cookies


def sign_in(cookies: requests.cookies.RequestsCookieJar):
    """签到"""
    session.cookies = cookies
    res = session.get('https://geekhub.com/checkins/')
    pattern = r'<meta name="csrf-token" content="(.*?)" />'
    result = re.search(pattern=pattern, string=str(res.text)).group(1)
    url = 'https://geekhub.com/checkins/start'
    data = {
        "_method": 'post',
        "authenticity_token": result
    }
    res = session.post(url=url, data=data)
    if "今日已签到" in res.text:
        print("签到成功")


def fetch_cookies() -> requests.cookies.RequestsCookieJar:
    if os.path.exists(COOKIES_PATH):
        with open(COOKIES_PATH, 'r') as f:
            cookies_dict = json.load(f)
            cookies = requests.utils.cookiejar_from_dict(cookies_dict)
            print('读取本地cookies')
            return cookies
    else:
        token = authenticity_token()
        _rucaptcha()
        cookies = login(token)
        return cookies


def main():
    cookies = fetch_cookies()
    sign_in(cookies)


if __name__ == '__main__':
    main()
