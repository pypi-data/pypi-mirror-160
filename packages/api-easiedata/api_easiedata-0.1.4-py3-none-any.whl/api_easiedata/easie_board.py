import gzip
import io
import json
import os
import pandas as pd
import requests
import time

class EasieBoard():
    
    def __getitem__(self, k):
        try:
            return getattr(self, k)
        except:
            return None

    def __init__(
        self, username, developer_key, url_api="https://api.easiedata.com",
        workspace_abs_path=None):

        self.url_api = url_api
        self.username = username
        self.developer_key = developer_key

        if workspace_abs_path is None:
            workspace_abs_path = os.getcwd()

        self.path = workspace_abs_path + '/'
        self.headers = {
            'Authorization': {
                'username': self.username,
                'developer_key':self.developer_key
            }
        }
        self.res = None

    def __str__(self):
        if self.res is None:
            return ''

        str_res = self.res.copy()
        str_res['http_status'] = self.http_status
        return json.dumps(str_res)

    def load_easieboard(self, board_name):
        headers = self.headers.copy()
        headers['Authorization']['board_name'] = board_name + ' @' + self.username
        headers['Authorization'] = json.dumps(headers['Authorization'])

        r = requests.post(
            self.url_api + '/developer/easieboard/load',
            headers=headers
        )

        self.http_status = r.status_code
        self.res = r.json()
        self.group_list = None

        if self.http_status == 200:
            self.group_list = self.res['data']
            self.res = {
                'success': True,
                'front_msg': 'Success!'
            }

        return self

    def get_group_list_values(self, board_name, data):
        headers = self.headers.copy()
        headers['Authorization']['board_name'] = board_name + ' @' + self.username
        headers['Authorization'] = json.dumps(headers['Authorization'])

        r = requests.post(
            self.url_api + '/developer/get_group_list_values',
            headers=headers,
            data=json.dumps(data)
        )

        self.http_status = r.status_code
        self.res = r.json()

        if self.http_status == 200:
            self.group_list_values = self.res['data']['group_list_values']
            self.res = {
                'success': True,
                'front_msg': 'Success!'
            }

        return self

