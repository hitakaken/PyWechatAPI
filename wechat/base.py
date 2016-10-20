# -*- coding: utf-8 -*-

"""
File:   base.py
Author: CaoKe
Email:  hitakaken@gmail.com
Github: https://github.com/hitakaken
Date:   2016-08-23
Description: WeChat HttpClient Base
"""

import datetime
import json
import requests
from urllib import quote

EXPIRED_LEEWAY = 60
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
ACCESS_TOKEN_QUERY_PARAMS = ['grant_type', 'appid', 'secret']


class BaseAPI(object):
    def __init__(self, **kwargs):
        self.defaults = kwargs
        self.session = requests.Session()
        self.access_token = None
        self.access_token_expired = None
        if 'retry' in self.defaults:
            from requests.adapters import HTTPAdapter
            self.session.mount('http://', HTTPAdapter(max_retries=self.defaults['retry']))
            self.session.mount('https://', HTTPAdapter(max_retries=self.defaults['retry']))

    def validate_required_params(self, required_params, **kwargs):
        missing = []
        for param in required_params:
            if param not in kwargs and param not in self.defaults:
                missing.append(param)
        return len(missing) == 0, missing

    def get_url(self, url, params=None, **kwargs):
        if params is not None:
            query = []
            for param in params:
                value = kwargs[param] if param in kwargs else self.defaults.get(param, None)
                if value is not None:
                    query.append(param + '=' + quote(value))
            url = url + '?' + '&'.join(query)
        return url

    def get(self, url, params=None, **kwargs):
        return self.session.get(self.get_url(url, params=params, **kwargs))

    def get_json(self, url, params=None,**kwargs):
        resp = self.get(url, params=params, **kwargs)
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        if 'errcode' in result:
            raise Exception(resp.text)
        return result

    def post(self, url, payload, params=None, **kwargs):
        return self.session.post(self.get_url(url, params=params, **kwargs), json=payload)

    def post_json(self, url, payload, params=None, **kwargs):
        resp = self.post(url, payload, params=params, **kwargs)
        resp.encoding = 'utf-8'
        result = json.loads(resp.text)
        if 'errcode' in result:
            raise Exception(resp.text)
        return result

    def get_access_token(self):
        now = datetime.datetime.now()
        if self.access_token is None or self.access_token_expired is None or now > self.access_token_expired:
            result = self.get_json(
                ACCESS_TOKEN_URL,
                params=ACCESS_TOKEN_QUERY_PARAMS,
                grant_type='client_credential')
            self.access_token = result['access_token']
            expired_in = result['expires_in'] - EXPIRED_LEEWAY
            self.access_token_expired = now + datetime.timedelta(seconds=expired_in)
        return self.access_token
