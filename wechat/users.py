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
USER_INFO_URL = 'https://api.weixin.qq.com/cgi-bin/user/info'
USER_INFO_QUERY_PARAMS = ['access_token', 'openid', 'lang']
USER_INFO_BATCH_URL = 'https://api.weixin.qq.com/cgi-bin/user/info/batchget'
USER_INFO_BATCH__QUERY_PARAMS = ['access_token']
TAGS_URL = "https://api.weixin.qq.com/cgi-bin/tags/get"
TAGS_QUERY_PARAMS = ['access_token']


class UsersAPI(BaseAPI):
    """用户管理"""
    def __init__(self, **kwargs):
        super(UsersAPI, self).__init__(**kwargs)

    def get_users(self, next_openid=None):
        """获取用户列表

        公众号可通过本接口来获取帐号的关注者列表，
        关注者列表由一串OpenID（加密后的微信号，
        每个用户对每个公众号的OpenID是唯一的）组成。
        一次拉取调用最多拉取10000个关注者的OpenID，可以通过多次拉取的方式来满足需求。

        接口调用请求说明
        http请求方式: GET（请使用https协议）
        https://api.weixin.qq.com/cgi-bin/user/get?access_token=ACCESS_TOKEN&next_openid=NEXT_OPENID
        参数	是否必须	说明
        access_token	是	调用接口凭证
        next_openid	是	第一个拉取的OPENID，不填默认从头开始拉取

        返回说明
        正确时返回JSON数据包：
        {"total":2,"count":2,"data":{"openid":["","OPENID1","OPENID2"]},"next_openid":"NEXT_OPENID"}
        参数	说明
        total	关注该公众账号的总用户数
        count	拉取的OPENID个数，最大值为10000
        data	列表数据，OPENID的列表
        next_openid	拉取列表的最后一个用户的OPENID

        错误时返回JSON数据包（示例为无效AppID错误）：
        {"errcode":40013,"errmsg":"invalid appid"}

        附：关注者数量超过10000时
        当公众号关注者数量超过10000时，可通过填写next_openid的值，从而多次拉取列表的方式来满足需求。
        具体而言，就是在调用接口时，将上一次调用得到的返回中的next_openid值，作为下一次调用中的next_openid值。
        """
        result = self.get_json(USERS_URL, params=USERS_QUERY_PARAMS,
                               access_token=self.get_access_token(), next_openid=next_openid)
        return result.get('data', {}).get('openid', []), \
               result['total'], result['count'], result.get('next_openid', None)

    def get_user(self, openid=None):
        """获取用户基本信息（包括UnionID机制）

        开发者可通过OpenID来获取用户基本信息。请使用https协议。

        接口调用请求说明
        http请求方式: GET https://api.weixin.qq.com/cgi-bin/user/info?access_token=ACCESS_TOKEN&openid=OPENID&lang=zh_CN
        参数说明
        参数	是否必须	说明
        access_token	是	调用接口凭证
        openid	是	普通用户的标识，对当前公众号唯一
        lang	否	返回国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语

        返回说明
        正常情况下，微信会返回下述JSON数据包给公众号：
        参数说明
        参数	说明
        subscribe	用户是否订阅该公众号标识，值为0时，代表此用户没有关注该公众号，拉取不到其余信息。
        openid	用户的标识，对当前公众号唯一
        nickname	用户的昵称
        sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
        city	用户所在城市
        country	用户所在国家
        province	用户所在省份
        language	用户的语言，简体中文为zh_CN
        headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
        subscribe_time	用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
        unionid	只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
        remark	公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注
        groupid	用户所在的分组ID（兼容旧的用户分组接口）
        tagid_list	用户被打上的标签ID列表

        错误时微信会返回错误码等信息，JSON数据包示例如下（该示例为AppID无效错误）:
        {"errcode":40013,"errmsg":"invalid appid"}
        """
        return self.get_json(USER_INFO_URL, params=USER_INFO_QUERY_PARAMS,
                             access_token=self.get_access_token(), openid=openid, lang='zh_CN')

    def batch_get_user(self, openids=None):
        """批量获取用户基本信息

        开发者可通过该接口来批量获取用户基本信息。最多支持一次拉取100条。

        接口调用请求说明
        http请求方式: POST
        https://api.weixin.qq.com/cgi-bin/user/info/batchget?access_token=ACCESS_TOKEN
        参数说明
        参数	是否必须	说明
        openid	是	用户的标识，对当前公众号唯一
        lang	否	国家地区语言版本，zh_CN 简体，zh_TW 繁体，en 英语，默认为zh-CN

        返回说明
        正常情况下，微信会返回下述JSON数据包给公众号（示例中为一次性拉取了2个openid的用户基本信息，第一个是已关注的，第二个是未关注的）：
        参数说明
        参数	说明
        subscribe	用户是否订阅该公众号标识，值为0时，代表此用户没有关注该公众号，拉取不到其余信息，只有openid和UnionID（在该公众号绑定到了微信开放平台账号时才有）。
        openid	用户的标识，对当前公众号唯一
        nickname	用户的昵称
        sex	用户的性别，值为1时是男性，值为2时是女性，值为0时是未知
        city	用户所在城市
        country	用户所在国家
        province	用户所在省份
        language	用户的语言，简体中文为zh_CN
        headimgurl	用户头像，最后一个数值代表正方形头像大小（有0、46、64、96、132数值可选，0代表640*640正方形头像），用户没有头像时该项为空。若用户更换头像，原有头像URL将失效。
        subscribe_time	用户关注时间，为时间戳。如果用户曾多次关注，则取最后关注时间
        unionid	只有在用户将公众号绑定到微信开放平台帐号后，才会出现该字段。
        remark	公众号运营者对粉丝的备注，公众号运营者可在微信公众平台用户管理界面对粉丝添加备注
        groupid 用户所在的分组ID（暂时兼容用户分组旧接口）
        tagid_list	用户被打上的标签ID列表

        错误时微信会返回错误码等信息，JSON数据包示例如下（该示例为AppID无效错误）:
        {"errcode":40013,"errmsg":"invalid appid"}
        """
        if openids is None:
            return []
        payload = {"user_list": map(lambda openid:{"openid":openid, "lang":"zh-CN"}, openids)}
        return self.post_json(USER_INFO_BATCH_URL, payload, params=USER_INFO_BATCH__QUERY_PARAMS,
                              access_token=self.get_access_token()).get("user_info_list")

    def get_tags(self):
        """获取公众号已创建的标签

        接口调用请求说明
        http请求方式：GET（请使用https协议）
        https://api.weixin.qq.com/cgi-bin/tags/get?access_token=ACCESS_TOKEN

        返回说明
        参数说明
        参数	说明
        id	标签唯一标示
        name 名称
        count 此标签下粉丝数
        """
        return self.get_json(TAGS_URL, params=TAGS_QUERY_PARAMS,
                             access_token=self.get_access_token()).get("tags", [])

