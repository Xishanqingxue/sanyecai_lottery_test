# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class JoinProjectApi(LoginBaseApi):
    """
    合买策略的数据接口（返回合买人数、窗口个数）
    """
    url = "/info/joinProject"

    def build_custom_param(self, data):
        return {'projectId':data['projectId']}