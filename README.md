# PyWechatAPI

[微信公众号](https://mp.weixin.qq.com)开发 Python API

## 快速开始
1. 安装PyWechatAPI(*还未上传)
```
pip install PyWechatAPI
```
2. 调用API示例
```python
# 初始化客户端
from flask import request 
from wechat.client import WechatAPI

wechat = WechatAPI(
    appid={{APPID}},  # 公众号唯一标识
    secret={{SECRET}},  # 公众号授权密钥
    redirect_uri={{REDIRECT_URI}}  # 回调处理请求地址
)
```
3. 网页授权示例
```python
# 第一步，获取微信授权网址，可带上用户识别参数
authorize_url = wechat.get_authorize_url(state='User:%s' % ({{USER_ID}}))
# 将用户重定向到authorize_url，由用户在微信界面进行授权
# 授权结束，微信服务器会发送回调请求到 {{REDIRECT_URI}}
# 回调请求形如：HTTP GET {{REDIRECT_URI}}/?code=CODE&state=STATE

# 回调处理如下
# 首先判断用户是否授权 
authorized = wechat.is_authorized(request.args)
if not authorized:
    # Do something
    raise Exception('用户没有授权')    

# 第二步：通过code换取网页授权access_token
token = wechat.exchange_code(code=request.args['code']) # 请求失败会抛出异常

access_token = token['access_token']      # 网页授权接口调用凭证
expires_in = token['expires_in']          # access_token失效时间
refresh_token = token['refresh_token']    # 用户刷新access_token使用的令牌
openid = token['openid']                  # 用户唯一标识，每个公众号唯一，不同公众号不同
scope = token['scope']                    # 用户授权的作用域，使用逗号（,）分隔

# 第三步：刷新access_token（如果需要）
token = wechat.refresh_token(refresh_token=token['refresh_token'])

# 第四步：拉取用户信息(需scope为 snsapi_userinfo)
user_info = wechat.get_user_info(access_token=access_token, openid=openid)
```
