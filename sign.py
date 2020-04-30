import re
import requests

session = requests.Session()

# 获取authenticity_token
def authenticity_token():
    res = session.get('https://geekhub.com/users/sign_in')
    pattern = r'<form class="simple_form new_user" id="new_user" novalidate="novalidate" action="/users/sign_in" accept-charset="UTF-8" method="post"><input type="hidden" name="authenticity_token" value="(.*?)" />'
    result = re.findall(pattern=pattern, string=str(res.text))
    print(result)
    return result
# 获取验证码
def _rucaptcha():
    res = session.get('https://geekhub.com/rucaptcha/')
    with open('123.jpg', 'wb') as f:
        f.write(res.content)
# 登录
def login(authenticity_token):
    data = {
        "authenticity_token": authenticity_token[0],
        "user[login]": 'XXX', # 用户名
        "user[password]": 'XXX', # 密码
        "_rucaptcha": input('请输入验证码:'),
        "user[remember_me]": 'on'
    }
    url = 'https://geekhub.com/users/sign_in'
    res = session.post(url=url, data=data)
    if "退出" in res.text:
        print("登录成功")
# 签到
def sign_in():
    res = session.get('https://geekhub.com/checkins/')
    pattern = r'<meta name="csrf-token" content="(.*?)" />'
    result = re.findall(pattern=pattern, string=str(res.text))
    url = 'https://geekhub.com/checkins/start'
    data ={
        "_method": 'post',
        "authenticity_token": result[0]
    }
    res =session.post(url=url, data=data)
    if "今日已签到" in res.text:
        print("签到成功")
def main():
    a = authenticity_token() # 获取authenticity_token
    _rucaptcha()             # 获取验证码
    login(a)                 # 登录
    sign_in(a)               # 签到

if __name__ == '__main__':
    main()
