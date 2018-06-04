# # -*- coding:utf-8 -*-
# from base_api.bet_api import BetBetApi
# from base.base_case import BaseCase
# from base_api.join_detail_api import JoinDetailApi
# from base_api.join_project_api import JoinProjectApi
# from base_api.my_ac_det_api import MyAcDetApi
# from base_api.my_join_api import MyJoinApi
# from utilities.redis_helper import Redis
# from utilities.mysql_helper import MysqlHelper
# import time
# import settings
# import json
#
#
# class TestMyJoinApi(BaseCase):
#     """
#     我的合买记录
#     """
#     union_id = settings.TEST_UNION_ID
#     user_id = MysqlHelper().get_user_details(union_id)['id']
#     stock_id = 1
#     room_id = 1
#
#     def setUp(self):
#         MysqlHelper().fix_user_money(balance=10000, user_id=self.user_id)
#
#
#     def test_get_my_join_success(self):
#         bet_api = BetBetApi(self.union_id)
#         bet_api.get({"lotoId": self.stock_id, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
#                      "memberNum": 2, 'provinceId': 1})
#         self.assertEqual(bet_api.get_resp_code(), 200)
#         self.assertEqual(bet_api.get_resp_message(), u"下单成功")
#
#         my_join_api = MyJoinApi(self.union_id)
#         response = my_join_api.get({'status': None, 'page': 1, 'length': 10})
#         resp = json.loads(response.text)
#
#         self.assertEqual(my_join_api.get_resp_code(), 200)
#         self.assertEqual(my_join_api.get_resp_message(), u'success')
#
#         result = my_join_api.get_resp_result()
#         project_id = result[0]['projectNo']
#
#         join_rank_today_api = JoinDetailApi(self.union_id)
#         response = join_rank_today_api.get({'projectId':project_id,'page':1,'length':50})
#         resp = json.loads(response.text)
#
#         self.assertEqual(join_rank_today_api.get_resp_code(),200)
#
#         # join_project_api = JoinProjectApi(self.union_id)
#         # response = join_project_api.get({'projectId':project_id})
#         # resp = json.loads(response.text)
#         #
#         # self.assertEqual(join_project_api.get_resp_code(),200)
#
#         my_ac_det_api = MyAcDetApi(self.union_id)
#         response = my_ac_det_api.get({'unionId':self.union_id,'source':1})
#         resp = json.loads(response.text)
#
#         self.assertEqual(my_ac_det_api.get_resp_code(),200)
#
#
#     def tearDown(self):
#         mysql = MysqlHelper()
#         mysql.delete_lot_order(self.user_id)
#         Redis().fix_stock_day_cache(stock_id=self.stock_id, num=10000)
#         mysql.fix_user_money(balance=0, user_id=self.user_id)
#         mysql.delete_account_details(self.user_id)
#         time.sleep(2)