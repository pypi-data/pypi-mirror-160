# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import requests, json

class quantim:
    def __init__(self, username, password, secretpool, env="qa"):
        self.username = username
        self.password = password
        self.secretpool = secretpool
        self.env = env

    def get_header(self):
        token_url = "https://api-quantimqa.sura-im.com/tokendynamicpool" if self.env=="qa" else "https://api-quantim.sura-im.com/tokendynamicpool"
        data = {"username":self.username, "password":self.password, "secretpool":self.secretpool}
        headers = {"Accept": "*/*",'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        access_token_response = requests.post(token_url, data=json.dumps(data), headers=headers, verify=False, allow_redirects=False)
        tokens = json.loads(access_token_response.text)
        access_token = tokens['id_token']
        api_call_headers = {"Accept": "*/*", 'Authorization': 'Bearer ' + access_token, 'Content-Type': 'application/json', 'Access-Control-Allow-Origin': '*'}
        return api_call_headers

    def api_call(self, endpoint, method="post", data=None, verify=False):
        api_call_headers = self.get_header()
        api_url = f"{'https://api-quantimqa.sura-im.com/' if self.env=='qa' else 'https://api-quantim.sura-im.com/'}{endpoint}"
        if method.lower()=='post':
            api_call_response = requests.post(api_url, headers=api_call_headers, data=json.dumps(data), verify=verify)
        elif method.lower()=='get':
            api_call_response = requests.post(test_api_url, headers=api_call_headers, data=data, verify=verify)
        else:
            print("Method not supported!")
            return None
        return json.loads(api_call_response.text)
