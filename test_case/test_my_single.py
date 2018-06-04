# # -*- coding:utf-8 -*-
# from base_api.my_single_api import MySingleApi
# from base_api.bet_api import BetBetApi
# from base.base_case import BaseCase
# from base import base_helper
# from utilities.mysql_helper import MysqlHelper
# from utilities.redis_helper import Redis
# import time, settings
# from base_api.get_online_api import GetOnlineApi
# from base_api.bet_get_sell_lott_api import BetGetSellLottApi
#
#
# class TestMySingleApi(BaseCase):
#     """
#     我的单买(自买)记录列表（待开奖、已中奖、未中奖）
#     """
#     # 待开奖status=0、已中奖(小奖status=2，大奖status=3）、未中奖status=1，None为全部信息
#     union_id = settings.TEST_UNION_ID
#     user_id = settings.TEST_USER_ID
#     source = 1
#     stock_id = 1
#
#     def setUp(self):
#         MysqlHelper().fix_user_money(balance=100000, user_id=self.user_id)
#
#     def test_my_single(self):
#         """
#         测试用户单买待开奖列表信息
#         :return:
#         """
#         # 调投注接口,代购3张
#         bet_api = BetBetApi(self.union_id)
#         bet_api.get({"lotoId": self.stock_id, "nums": 3, "buyType": 0, "window": 0, "roomId": 1, "shareMethod": None,
#                      "memberNum": None, 'provinceId': None})
#         self.assertEqual(bet_api.get_resp_code(), 200)
#         self.assertEqual(bet_api.get_resp_message(), "下单成功")
#
#         my_single = MySingleApi(self.union_id)
#         my_single.get({'unionId':self.union_id,'source':self.source,'status':0})
#         self.assertEqual(my_single.get_resp_code(),200)
#         self.assertEqual(my_single.get_resp_message(),"success")
#         result = my_single.get_resp_result()
#         order_id = []
#         for i in range(len(result)):
#             order_id.append(result[i]['id'])
#         # 校验内容
#         order_list = MysqlHelper().get_lot_order(result[0]["userId"])
#         self.assertEqual(result[0]["orderNo"],order_list[0]["order_no"])
#         self.assertEqual(result[0]["lotteryId"], order_list[0]["lottery_id"])
#
#         get_sell_lott = BetGetSellLottApi()
#         get_sell_lott.get()
#         self.assertEqual(get_sell_lott.get_resp_code(), 200)
#         result_lott = get_sell_lott.get_resp_result()
#         for i in range(len(result_lott)):
#             id = result_lott[i]["id"]
#             lotteryId = result[0]["lotteryId"]
#             if id==lotteryId:
#                 self.assertEqual(result[0]["lotteryName"], result_lott[i]["lotteryName"])
#
#         self.assertEqual(result[0]["buyType"], order_list[0]["buy_type"])
#         self.assertEqual(result[0]["orderStatus"], order_list[0]["order_status"])
#         self.assertEqual(result[0]["bonusStatus"], order_list[0]["bonus_status"])
#         self.assertEqual(result[0]["stationNum"], order_list[0]["station_num"])
#         self.assertEqual(result[0]["num"], order_list[0]["num"])
#         self.assertEqual(result[0]["amount"], order_list[0]["amount"])
#
#         get_online = GetOnlineApi(self.union_id)
#         get_online.get()
#         self.assertEqual(get_online.get_resp_code(), 200)
#         result_online = get_online.get_resp_result()
#         self.assertEqual(result[0]["userName"], result_online["user"]["userName"])
#
#         odList = result[0]["odList"]
#         all_list = MysqlHelper().get_order_details(order_id[0])
#         self.assertEqual(odList[0]["seq"], all_list["seq"])
#         self.assertEqual(odList[0]["detailStatus"], all_list["detail_status"])
#         self.assertEqual(odList[0]["amount"], all_list["amount"])
#         self.assertEqual(odList[0]["bonusStatus"], all_list["bonus_status"])
#         self.assertEqual(odList[0]["bonusAmount"], all_list["bonus_amount"])
#         self.assertEqual(odList[0]["bonusTime"], all_list["bonus_time"])
#         self.assertEqual(odList[0]["ticketNo"], all_list["ticket_no"])
#         self.assertEqual(odList[0]["route"], all_list["route"])
#         self.assertEqual(odList[0]["gpyId"], all_list["gpy_id"])
#         self.assertEqual(odList[0]["stationNumber"], all_list["station_number"])
#         createTime = base_helper.get_nums_in_string(str(odList[0]["createTime"]))
#         create_time = base_helper.get_nums_in_string(str(all_list["create_time"]))
#         self.assertEqual(createTime, create_time)
#
#         for i in order_id:
#             MysqlHelper().delete_order_details(i)
#
#     def tearDown(self):
#         mysql = MysqlHelper()
#         mysql.delete_lot_order(self.user_id)
#         Redis().fix_stock_day_cache(stock_id=self.stock_id, num=10000)
#         mysql.fix_user_money(balance=100000, user_id=self.user_id)
#         mysql.delete_account_details(self.user_id)
#         time.sleep(2)