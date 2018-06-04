# # -*- coding:utf-8 -*-
# from base_api.send_sms_message_api import SendSmsMessageApi
# from base_api.image_code_api import ImageCodeApi
# from base_api.bind_card_api import BindCardApi
# from utilities.mysql_helper import MysqlHelper
# from base_api.binding_list_api import BindingListApi
# from base.base_case import BaseCase
# from utilities.redis_helper import Redis
# import random,json
# import unittest
# import settings
#
#
# class TestBindCardApi(BaseCase):
#     """
#     绑定银行卡
#     """
#     union_id = settings.TEST_UNION_ID
#     not_authentication_union_id = 8887
#     auth_id = 8
#     mobile = '1511011' + str(random.randint(1111, 9999))
#
#     def test_bind_card_success(self):
#         """
#         测试绑定银行卡成功
#         :return:
#         """
#         mobile = '13511114758'
#         image_code_api = ImageCodeApi()
#         image_code_api.get({'mobile': mobile})
#
#         image_code = Redis().get_image_code(mobile)
#         sms_code_api = SendSmsMessageApi(self.union_id)
#         sms_code_api.get({'mobile': mobile, 'type': 'tj_sms_code', 'imgCode': image_code})
#
#         # self.assertEqual(sms_code_api.get_resp_code(), 200)
#
#         sms_code = Redis().get_sms_code(mobile, type='tj')
#
#         bind_card_api = BindCardApi(self.union_id)
#         bind_card_api.get({'bindingType': 1, 'cardNum': '6228480018373695875', 'bankId': 2,
#                 'mobile': mobile, 'verCode': sms_code, 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),200)
#
#         # 获取绑定列表
#         bind_list_api  = BindingListApi(self.union_id)
#         bind_list_api.get()
#         self.assertEqual(bind_list_api.get_resp_code(),200)
#         self.assertEqual(bind_list_api.get_resp_message(),u'ok')
#
#         result = bind_list_api.get_resp_result()[0]
#         self.assertEqual(result['bankId'],2)
#         self.assertEqual(result['bindingType'],1)
#         self.assertEqual(result['cardNum'],u'6228480018373695875')
#         self.assertEqual(result['bankName'],u'农业银行')
#
#     def test_bind_card_not_auth(self):
#         """
#         测试未实名认证绑定银行卡
#         :return:
#         """
#         mobile = '1870000' + str(random.randint(1111,9999))
#         image_code_api = ImageCodeApi()
#         image_code_api.get({'mobile': mobile})
#
#         image_code = Redis().get_image_code(mobile)
#         sms_code_api = SendSmsMessageApi(self.union_id)
#         sms_code_api.get({'mobile': mobile, 'type': 'tj_sms_code', 'imgCode': image_code})
#
#         # self.assertEqual(sms_code_api.get_resp_code(), 200)
#
#         sms_code = Redis().get_sms_code(mobile, type='tj')
#
#         bind_card_api = BindCardApi(self.not_authentication_union_id)
#         bind_card_api.get({'bindingType': 1, 'cardNum': '6228480018373695875', 'bankId': 2,
#                 'mobile': mobile, 'verCode': sms_code, 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),415)
#         self.assertEqual(bind_card_api.get_resp_message(),u'未实名认证,请先实名认证再绑定!')
#
#         # 获取绑定列表
#         bind_list_api = BindingListApi(self.union_id)
#         bind_list_api.get()
#         self.assertEqual(bind_list_api.get_resp_code(), 200)
#         self.assertEqual(bind_list_api.get_resp_message(), u'ok')
#         self.assertEqual(bind_list_api.get_resp_result(),[])
#
#     def test_bind_card_again(self):
#         """
#         测试绑定银行卡重复绑定
#         :return:
#         """
#         mobile = '13511114758'
#         image_code_api = ImageCodeApi()
#         image_code_api.get({'mobile': mobile})
#
#         image_code = Redis().get_image_code(mobile)
#         sms_code_api = SendSmsMessageApi(self.union_id)
#         sms_code_api.get({'mobile': mobile, 'type': 'tj_sms_code', 'imgCode': image_code})
#
#         # self.assertEqual(sms_code_api.get_resp_code(), 200)
#
#         sms_code = Redis().get_sms_code(mobile, type='tj')
#
#         bind_card_api = BindCardApi(self.union_id)
#         bind_card_api.get({'bindingType': 1, 'cardNum': '6228480018373695875', 'bankId': 2,
#                 'mobile': mobile, 'verCode': sms_code, 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),200)
#
#         mobile = '13511114758'
#         image_code_api = ImageCodeApi()
#         image_code_api.get({'mobile': mobile})
#
#         image_code = Redis().get_image_code(mobile)
#         sms_code_api = SendSmsMessageApi(self.union_id)
#         sms_code_api.get({'mobile': mobile, 'type': 'tj_sms_code', 'imgCode': image_code})
#
#         # self.assertEqual(sms_code_api.get_resp_code(), 200)
#
#         sms_code = Redis().get_sms_code(mobile, type='tj')
#
#         bind_card_api = BindCardApi(self.union_id)
#         bind_card_api.get({'bindingType': 1, 'cardNum': '6228480018373695875', 'bankId': 2,
#                 'mobile': mobile, 'verCode': sms_code, 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),407)
#         self.assertEqual(bind_card_api.get_resp_message(),u'已绑定,无需再次绑定!')
#
#     @unittest.skip(reason=settings.SKIP_REASON)
#     def test_bind_card_binding_type_null(self):
#         """
#         测试请求接口bindingType为None
#         :return:
#         """
#         bind_card_api = BindCardApi(self.union_id)
#         bind_card_api.get({'bindingType': None, 'cardNum': '6228480018373695875', 'bankId': 2,
#                 'mobile': self.mobile, 'verCode': '1234', 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),200)
#
#     @unittest.skip(reason=settings.SKIP_REASON)
#     def test_bind_card_card_num_null(self):
#         """
#         测试请求接口cardNum为None
#         :return:
#         """
#         bind_card_api = BindCardApi(self.union_id)
#         bind_card_api.get({'bindingType': 1, 'cardNum': None, 'bankId': 2,
#                 'mobile': self.mobile, 'verCode': '1234', 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),200)
#
#     def test_bind_card_bank_id_null(self):
#         """
#         测试请求接口bindingType为None,可以绑定成功
#         :return:
#         """
#         mobile = '13511114758'
#         image_code_api = ImageCodeApi()
#         image_code_api.get({'mobile': mobile})
#
#         image_code = Redis().get_image_code(mobile)
#         sms_code_api = SendSmsMessageApi(self.union_id)
#         sms_code_api.get({'mobile': mobile, 'type': 'tj_sms_code', 'imgCode': image_code})
#
#         # self.assertEqual(sms_code_api.get_resp_code(), 200)
#
#         sms_code = Redis().get_sms_code(mobile, type='tj')
#
#         bind_card_api = BindCardApi(self.union_id)
#         bind_card_api.get({'bindingType': 1, 'cardNum': '6228480018373695875', 'bankId': None,
#                 'mobile': mobile, 'verCode': sms_code, 'type': 'tj_sms_code'})
#
#         self.assertEqual(bind_card_api.get_resp_code(),200)
#         self.assertEqual(bind_card_api.get_resp_message(),u'绑定成功!')
#
#     def tearDown(self):
#         MysqlHelper().delete_bind_card(self.auth_id)