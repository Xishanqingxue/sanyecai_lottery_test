# # -*- coding:utf-8 -*-
# from base_api.bet_get_sell_lott_api import BetGetSellLottApi
# from base.base_case import BaseCase
# from utilities.mysql_helper import MysqlHelper
#
#
# class TestBetGetSellLottApi(BaseCase):
#     """
#     获取在售彩种列表
#     """
#
#     def test_get_self_lott_success(self):
#         """
#         获取在售彩种成功
#         :return:
#         """
#         get_sell_lott = BetGetSellLottApi()
#         get_sell_lott.get()
#         self.assertEqual(get_sell_lott.get_resp_code(), 200)
#         result = get_sell_lott.get_resp_result()
#         for i in range(len(result)):
#             id = result[i]["id"]
#             one_lottery = MysqlHelper().get_sell_lottery_list(id)
#             self.assertEqual(result[i]["lotteryName"], one_lottery["lottery_name"])
#             self.assertEqual(result[i]["denomination"], one_lottery["denomination"])
#             self.assertEqual(result[i]["salesStatus"], one_lottery["sales_status"])
#             self.assertEqual(result[i]["maxBonus"], one_lottery["max_bonus"])
#             self.assertEqual(result[i]["lotteryName"], one_lottery["lottery_name"])
#             # 获取省份的名字
#             province_id = one_lottery["province_id"]
#             province_name = MysqlHelper().get_province_name(province_id)
#             self.assertEqual(result[i]["province"], province_name["name"])
