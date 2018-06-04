# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi


class MyPrecentApi(LoginBaseApi):
    """
    获取提现记录
    """
    url = "/info/myPrecent"

    def build_custom_param(self, data):
        return {'page': data['page'], 'length': data['length']}
