import requests
import json
import urllib
from urllib.parse import urlencode
import base64
import rsa
import binascii
import re

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537.36'
}
session = requests.Session()

def get_su(user_name):
    su = base64.b64encode(user_name.encode(encoding='utf-8'))
    return su.decode('utf-8')

def get_data(su):
    param = {
        'entry':'weibo',
        'rsakt':'mod',
        'checkpin':'1',
        'client':'ssologin.js(v1.4.18)',
        '_':'1461819359582',
        'su':su
    }
    url = 'http://login.sina.com.cn/sso/prelogin.php?' + urlencode(param)
    response = session.get(url,headers=headers)
    response.encoding = 'utf-8'
    data = json.loads(response.text)
    return get_param(data)

def get_param(data):
    servertime = data['servertime']
    nonce = data['nonce']
    rsakv = data['rsakv']
    pubkey = data['pubkey']
    return (servertime,nonce,rsakv,pubkey)

def get_sp(param,password):
    rsaPublicKey = int(param[3],16)
    key = rsa.PublicKey(rsaPublicKey,65537)
    message = str(param[0]) + '\t' + str(param[1]) + '\n' + str(password)
    sp = binascii.b2a_hex(rsa.encrypt(message.encode(encoding='utf-8'),key))
    return sp

def post_data(su,sp,param):
    url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)'
    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from':'',
        'savestate': '0',
        'useticket': '1',
        'vsnf': '1',
        'su': su,
        'service':'miniblog',
        'servertime': param[0],
        'nonce': param[1],
        'pwencode': 'rsa2',
        'rsakv': param[2],
        'sp': sp,
        'sr': '1536 * 864',
        'encoding': 'UTF - 8',
        'prelt': '69',
        'url': 'https://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }
    response = session.post(url,data=postdata,headers=headers)
    response.encoding = 'gbk'
    return response.text

def login(html):
    pattern = r'location\.replace\([\'"](.*?)[\'"]\)'
    url = re.findall(pattern, html)[0]
    session.get(url, headers=headers)

def test():
    url = 'https://d.weibo.com/'
    response = session.get(url,headers=headers)
    print(response.text)

    # param = {
    #     'access_token':'',
    #     'uid':'1001030101',
    # }
    # url = 'https://api.weibo.com/2/eps/user/info.json' + urlencode(param)
    # response = requests.get(url)
    # print(response.text)


def main(username,password):
    su = get_su(username)
    param = get_data(su)
    sp = get_sp(param,password)
    html = post_data(su,sp,param)
    login(html)

if __name__ == '__main__':
    username = '13717523878'
    password = '13717523878'
    main(username,password)