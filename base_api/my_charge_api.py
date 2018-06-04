# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class MyChargeApi(LoginBaseApi):
    """
    我的充值记录
    """
    url = "/info/myCharge"

    def build_custom_param(self, data):
        return {'page':data['page'],'length':data['length']}