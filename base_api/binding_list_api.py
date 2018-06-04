# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class BindingListApi(LoginBaseApi):
    """
    查询用户绑定列表
    """
    url = "/finan/queryBindingList"