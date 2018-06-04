# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class InfoMySingleLotApi(LoginBaseApi):
    """
    我的购彩记录（单买）
    """
    url = "/info/mySingleLot"

    def build_custom_param(self, data):
        return {'unionId':data['unionId'],'source':data['source'],'detailStatus':data['detailStatus'],
                'bonusStatus':data['bonusStatus'],'page':data['page'],'length':data['length']}