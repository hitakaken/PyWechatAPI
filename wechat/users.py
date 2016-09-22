# -*- coding: utf-8 -*-

"""
File:   users.py
Author: CaoKe
Email:  hitakaken@gmail.com
Github: https://github.com/hitakaken
Date:   2016-08-23
Description: WeChat User API
"""

from wechat.base import BaseAPI

USERS_URL = 'https://api.weixin.qq.com/cgi-bin/user/get'
USERS_QUERY_PARAMS = ['access_token', 'next_openid']


class UsersAPI(BaseAPI):
    def __init__(self, **kwargs):
        super(UsersAPI, self).__init__(**kwargs)

    def get_users(self, next_openid=None):
        result = self.get_json(USERS_URL, params=USERS_QUERY_PARAMS,
                               access_token=self.get_access_token(), next_openid=next_openid)
        return result.get('data', {}).get('openid', []), \
               result['total'], result['count'], result['next_openid']
