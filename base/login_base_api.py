# -*- coding:utf-8 -*-
from base_api.login_api import LoginApi
from base.base_api import BaseApi
from base.base_log import BaseLogger
import requests
import settings
import json

logger = BaseLogger(__name__).get_logger()


class LoginBaseApi(BaseApi):

    def __init__(self, union_id, nickname=settings.TEST_NICKNAME, source=settings.TEST_SOURCE,
                 head_pic=settings.TEST_HEAD_PIC, *args, **kwargs):
        super(LoginBaseApi, self).__init__(*args, **kwargs)
        self.union_id = union_id
        self.source = source
        self.nickname = nickname
        self.head_pic = head_pic

    def get_token(self):
        """
        获取token
        :return:
        """
        token = LoginApi().login(unionID=self.union_id, source=self.source, nickname=self.nickname,
                                 head_pic=self.head_pic, only_token=True)
        return token

    def get(self, data=None):
        """
        请求方式：GET
        :param data:
        :return:
        """
        token = self.get_token()
        request_data = self.format_param(data)
        logger.info('Data:{0}'.format(request_data))
        s = requests.session()
        s.cookies.set('VIDEO_LOTTERY_CODE_TOKEN_ID', token)
        self.response = s.get(url=self.api_url(), params=request_data, headers=self.headers)
        logger.info('Headers:{0}'.format(self.response.request.headers))
        logger.info('Response:{0}'.format(self.response.text))
        return self.response
