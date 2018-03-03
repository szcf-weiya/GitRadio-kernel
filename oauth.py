# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 00:52:03 2018

@author: weiya
"""

import requests
import json
import base64
#from urllib.parse import quote
## the two vars can be found in your own sina app
app_key = 'APP KEY'
app_secret = 'APP SECRET'
## you need to setup the callback url in your own sina app
callback_url = 'CALLBACK URL'
## your sina username
username = '****'
## your sina passwd
passwd = '****'
headers = {'User-Agent':"Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0"}

def login(username, password):
    username = base64.b64encode(username.encode('utf-8')).decode('utf-8')
    postData = {
            "entry": "sso",
            "gateway": "1",
            "from": "null",
            "savestate": "30",
            "useticket": "0",
            "pagerefer": "",
            "vsnf": "1",
            "su": username,
            "service": "sso",
            "sp": password,
            "sr": "1440*900",
            "encoding": "UTF-8",
            "cdult": "3",
            "domain": "sina.com.cn",
            "prelt": "0",
            "returntype": "TEXT",
        }
    loginURL = r'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)'
    session = requests.Session()
    
    res = session.post(loginURL, data = postData, headers = headers)
    jsonStr = res.content.decode('gbk')
    info = json.loads(jsonStr)
    if info["retcode"] == "0":
        print("Login Success!")
        
        cookies = session.cookies.get_dict()
        cookies = [key + "=" + value for key, value in cookies.items()]
        cookies = "; ".join(cookies)
        session.headers["cookie"] = cookies
    else:
        print("Login Failed，resons： %s" % info["reason"])
    return session

## redirect to authorize
def get_access_token(app_key, app_secret, callback_url, session):
    url = "https://api.weibo.com/oauth2/authorize?client_id={0}&response_type=code&redirect_uri={1}".format(app_key, callback_url)
    print(url)
    ## wait for user to login
    res = session.get(url)
    ## extract code
    tmp, code = res.url.split('code=')
    #url2 = "https://api.weibo.com/oauth2/access_token?client_id={0}&client_secret={1}&grant_type=authorization_code&redirect_uri={2}&code={3}".format(app_key, app_secret, callback_url, code)
    #res2 = session.get(url2) !! Atterntion the method should be POST, rather than GET
    url2 = "https://api.weibo.com/oauth2/access_token"
    postdata = {'client_id': app_key,
                'client_secret': app_secret,
                'grant_type': 'authorization_code',
                'redirect_uri': callback_url,
                'code': code}
    res2 = session.post(url2, data = postdata)
    ## get access_token
    access_token = res2.json()['access_token']
    return(access_token)

def new_weibo(access_token, content):
    postdata = {
            'access_token': access_token,
            'status': content
            }
    url = "https://api.weibo.com/2/statuses/share.json"
    res = requests.post(url, data=postdata, headers = headers)
    print(res.json())

def send_weibo(content):
    session = login(username, passwd)
    token = get_access_token(app_key, app_secret, callback_url, session)
    new_weibo(token, content)

if __name__ == '__main__':
    send_weibo("hello world!")