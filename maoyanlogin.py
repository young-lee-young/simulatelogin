#本代码同样适用于美团方面各个网站的模拟登陆

import requests
from urllib.parse import urlencode
import re
import time

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52'
}
session = requests.Session()

def pre_login():
    try:
        param = {
            'service':'maoyan',
            'continue':'http://maoyan.com/passport/login?redirect=%2F'
        }
        url = 'https://passport.meituan.com/account/unitivelogin?' + urlencode(param)
        response = session.get(url,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ConnectionError as e:
        print(e.args)
        print('预登陆出错')

def parse_param(html):
    try:
        pattern1 = re.compile(r'name="csrf" value="(.*?)"',re.S)
        pattern2 = re.compile(r'class="form-uuid" style="display:none">(.*?)</i>',re.S)
        pattern3 = re.compile(r'class="form-field J-form-field-captcha form-field--captcha" style="display:(.*?)"')
        csrf = re.search(pattern1,html).group(1)
        uuid = re.search(pattern2,html).group(1)
        need_captcha = re.search(pattern3,html).group(1)
        return (csrf,uuid,need_captcha)
    except:
        print('解析csrf,uuid,need_captcha出错')

def formal_login(username,password,param):
    csrf = param[0]
    uuid = param[1]
    if param[2] is 'none':
        captcha_param = {
            'uuid':uuid,
        }
        url = 'https://passport.meituan.com/account/captcha?' + urlencode(captcha_param)
        print(url)
        captcha = input('需要验证码:')
    else:
        captcha = ''
    url_param = {
        'uuid':uuid,
        'service':'maoyan',
        'continue': 'http://maoyan.com/passport/login?redirect=%2F',
    }
    postdata ={
        'email': username,
        'password': password,
        'captcha': captcha,
        'origin': 'account - login',
        'fingerprint': '',
        'csrf': csrf
    }
    url = 'https://passport.meituan.com/account/unitivelogin?' + urlencode(url_param)
    try:
        response = session.post(url,data=postdata,headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except ConnectionError as e:
        print(e.args)
        print('登录出错')

def parse_token(html):
    try:
        pattern = re.compile(r'name="token" type="hidden" value="(.*?)"',re.S)
        token = re.search(pattern,html).group(1)
        return token
    except:
        print('解析token出错')

def redirect_login(token):
    postdata = {
        'token': token,
        'expire': 0,
        'isdialog': 0,
        'autologin': 0,
        'logintype': 'normal'
    }
    try:
        url = 'http://maoyan.com/passport/login?redirect=%2F'
        session.post(url,data=postdata,headers=headers)
    except ConnectionError as e:
        print(e.args)
        print('重定向出错')

def test():
    try:
        time.sleep(5)
        url = 'http://maoyan.com/profile'
        response = session.get(url,headers=headers)
        print(response.status_code)
        print(response.text)
    except ConnectionError as e:
        print(e.args)
        print('测试出错')

def login(username,password):
    html_pre_login = pre_login()
    param = parse_param(html_pre_login)
    html_login = formal_login(username,password,param)
    token = parse_token(html_login)
    redirect_login(token)

if __name__ == '__main__':
    username = '18401681943'
    password = 'lyzy1314'
    login(username,password)