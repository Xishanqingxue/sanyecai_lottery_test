# -*- coding:utf-8 -*-
from base_api.my_ac_det_api import MyAcDetApi
from base.base_case import BaseCase
import settings

# class TestMyAcDetApi(BaseCase):
#     """
#     获取用户账户变动记录信息，账户金额增减的明细
#     """
#     union_id = settings.TEST_UNION_ID
#     def test_my_ac_det(self):
#         my_account = MyAcDetApi(self.union_id)
#         res = my_account.get({'unionId':self.union_id,'source':1})
#         self.assertEqual(my_account.get_resp_code(),200)
#         # result is None,please wait
#         result = my_account.get_resp_result()
#         print (111)