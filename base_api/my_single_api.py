# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class MySingleApi(LoginBaseApi):
    """
    我的单买(自买)记录列表（待开奖、已中奖、未中奖）
    """
    url = "/info/mySingle"

    def build_custom_param(self, data):
        return {'unionId':data['unionId'],'source':data['source'],'status':data['status']}