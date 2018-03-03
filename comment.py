# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 00:58:26 2018

@author: weiya

create comment for a particular weibo
"""

import requests

def comment(content):
    postdata = {
                'access_token': 'access_token',
                'id': 4213524437672536,
                'comment_ori': 1,
                'comment' : '测试 via python 2.7 (requests) again'
                }
    if content:
        postdata['comment'] = content
    url = 'https://api.weibo.com/2/comments/create.json'
    headers = {'User-Agent': "Mozilla/5.0 (hp-tablet; Linux; hpwOS/3.0.2; U; de-DE) AppleWebKit/534.6 (KHTML, like Gecko) wOSBrowser/234.40.1 Safari/534.6 TouchPad/1.0"}
    req = requests.post(url, data=postdata, headers = headers)
    print(req.content)

if __name__ == '__main__':
    comment("via server" + " --auto sync")