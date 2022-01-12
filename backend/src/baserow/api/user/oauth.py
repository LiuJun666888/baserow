import base64
from urllib.parse import urlencode, parse_qs,quote
import json
import requests
from django.conf import settings
from rest_framework import status,serializers
from rest_framework.response import Response


class OAuthFelo(object):
    """
    Felo认证辅助工具类
    """

    def __init__(self, client_id=None, client_secret=None, redirect_uri=None, state=None):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.state = state  # 用于保存登录成功后的跳转页面路径

    def get_Felo_url(self):
        # Felo登录url参数组建
        data_dict = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'state': self.state
        }

        # 构建url
        Felo_url = 'https://passport.felo.me/oauth/authorize?' + urlencode(data_dict)

        return Felo_url

    # 获取access_token值
    def get_access_token(self, code):
        # 向FELO服务器发请求，拿授权码交换令牌
        token_url = settings.FELO_TOKEN_URL
        # token_url = 'https://passport.felo.me/oauth/token'

        # 格式为： client_id: client_secret的base64编码
        basic = settings.FELO_CLIENT_ID + ':' + settings.FELO_CLIENT_SECRET
        basic_auth = str(base64.b64encode(basic.encode("utf-8")), 'utf-8')
        # 请求时在http请求头加上：Authorization: Basic
        headers = {'Authorization':"Basic " + basic_auth, }
        post_data = {
            # 'client_id': self.client_id,
            # 'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
            'grant_type': 'authorization_code',
            'code': code,
        }

        # 发送请求
        try:
            response = requests.post(token_url, data=post_data, headers=headers)  # 服务器向FELO服务器发起请求，请求结果返回在res中


            # 提取数据
            # access_token=FE04************************CCE2&expires_in=7776000&refresh_token=88E4************************BE14
            data = response.json()

            # print('请求地址:',response.url)
            # print('接口返回:',response.text)
        except:
            raise serializers.ValidationError('oauth请求失败')

        # 提取access_token
        access_token = data.get('access_token')

        if not access_token:
            raise serializers.ValidationError('access_token获取失败')
            # raise Exception('access_token获取失败')

        return access_token

    # 获取open_id值

    def get_open_id(self, access_token):

        # 构建请求url
        url = 'https://open.felo.me/sdk/user/current'
        headers = {'Authorization': "Bearer " + access_token, }

        # 发送请求
        try:
            response = requests.get(url,headers=headers)
        except:
            raise serializers.ValidationError('oauth请求失败')
            # raise Exception('Felo请求失败')
        # 提取数据
        try:
            # callback( {"user":{"openId":"xxxx"});
            # 获取openid
            # openid = response.json()['user']['openId']
            userinfo = response.json().get('user')
        except:
            raise serializers.ValidationError('openid获取失败')
            # raise Exception('openid获取失败')

        return userinfo
