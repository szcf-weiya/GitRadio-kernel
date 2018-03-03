# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 01:00:18 2018

@author: weiya
"""

from http.server import CGIHTTPRequestHandler, HTTPServer
import json
from oauth import send_weibo
from comment import comment
    
class webhooks(CGIHTTPRequestHandler):
    def do_GET(self):
        self.send_response(404)
        # header
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
        # message
        message = 'Not Found!'
        
        self.wfile.write(bytes(message, "utf8"))
        return
    
    def do_POST(self):
        self.data_string  = self.rfile.read(int(self.headers['Content-Length']))
        print(self.data_string)
        print(self.requestline)
        req = self.requestline.split()
        if (req[1] == '/deploy'):
            # response status code
            self.send_response(200)           
        else:
            self.send_response(404)
 
        # header
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # remove characters like %7B
        try:
            from urllib import unquote
        except ImportError:
            from urllib.parse import unquote
        rawstr = unquote(self.data_string.decode('utf8'))
        # remove `payload=`
        tmp, jsonStr = rawstr.split('payload=')
        data = json.loads(jsonStr)
        commit_comments = data['commits']
        for i in range(len(commit_comments)):
            txt = commit_comments[i]['message'].replace('+', ' ')
            print(txt)
            comment(txt + " --auto sync")
            send_weibo(txt + "https://esl.hohoweiya.xyz Auto Sync https://esl.szcfweiya.cn")
        
def run():
    print('starting server ...')
    server_address = ('', 8088)
    httpd = HTTPServer(server_address, webhooks)
    print('running server ...')
    httpd.serve_forever()
    
    
if __name__ == "__main__":
    run()
        