# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class JoinDetailApi(LoginBaseApi):
    """
    合买彩票详情
    """
    url = "/info/joinDetail"

    def build_custom_param(self, data):
        return {'projectId':data['projectId'],'page':data['page'],'length':data['length']}
