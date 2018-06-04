# -*- coding:utf-8 -*-
from base.login_base_api import LoginBaseApi

class BankListApi(LoginBaseApi):
    """
    获取银行列表
    """
    url = "/finan/queryBankList"
