# # -*- coding:utf-8 -*-
# from base_api.my_charge_api import MyChargeApi
# from base.base_case import BaseCase
# import settings
# import json
#
# class TestMyChargeApi(BaseCase):
#     """
#     获取充值记录
#     """
#     union_id = settings.TEST_UNION_ID
#
#     def test_get_my_charge_list(self):
#         """
#         测试获取充值记录成功
#         :return:
#         """
#         my_charge_api = MyChargeApi(self.union_id)
#         my_charge_api.get({'page':1,'length':10})
#
#         self.assertEqual(my_charge_api.get_resp_code(),200)
#
#         result = my_charge_api.get_resp_result()
#         self.assertEqual(len(result),1)
#
#         self.assertIsNotNone(result[0]['lotAccount'])
#         self.assertEqual(result[0]['amount'],100.00)
#         self.assertEqual(result[0]['actual'], 100.00)
#         self.assertEqual(result[0]['chargeStatus'], 3)
#         self.assertEqual(result[0]['source'], 1)
#         self.assertEqual(result[0]['notify'], 9)
#         self.assertIsNone(result[0]['chargeType'])
#         self.assertIsNone(result[0]['successTime'])
#         self.assertIsNone(result[0]['thirdSerial'])
#         self.assertIsNone(result[0]['bak'])