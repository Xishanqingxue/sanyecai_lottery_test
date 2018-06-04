# # -*- coding:utf-8 -*-
# from base_api.logout_api import LogoutApi
# from base.base_case import BaseCase
# import settings
#
#
# class TestLogout(BaseCase):
#     """
#     退出登录
#     """
#     union_id = settings.TEST_UNION_ID
#
#     def test_logout_success(self):
#         """
#         测试用户退出登录
#         :return:
#         """
#         logout_api = LogoutApi(self.union_id)
#         response = logout_api.get()
#
#         self.assertEqual(response.text, '')
