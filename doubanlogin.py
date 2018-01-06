import requests
import time
from bs4 import BeautifulSoup
import re
import json
from multiprocessing import Pool

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36 OPR/48.0.2685.52'
}
session = requests.Session()

def login(username,password):
    loginurl = 'https://accounts.douban.com/login'
    logindata = {
        'source': 'index_nav',
        'redir': 'https://www.douban.com',
        'form_email': username,
        'form_password': password,
        'login': u'登录'
    }
    response = session.post(loginurl, data=logindata, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    captcha = soup.find('img', id='captcha_image')
    if captcha:
        captcha_url = captcha['src']
        pattern = r'<input type="hidden" name="captcha-id" value="(.*?)"/'
        captcha_id = re.findall(pattern, response.text)
        print(captcha_url)
        captcha_text = input('please input:')
        logindata['captcha-solution'] = captcha_text
        logindata['captcha-id'] = captcha_id
        response2 = session.post(loginurl, data=logindata, headers=headers)
        cookies = response2.cookies
        print(cookies)

def main(username,password):
    login(username,password)

if __name__ == '__main__':
    username = '用户名'
    password = '密码'
    main()

