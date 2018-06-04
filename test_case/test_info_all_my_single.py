# -*- coding:utf-8 -*-
from base_api.my_single_lot_api import InfoMySingleLotApi
from base_api.bet_api import BetBetApi
from base.base_case import BaseCase
from base import base_helper
from utilities.mysql_helper import MysqlHelper
from utilities.redis_helper import Redis
import time, settings


class TestInfoMySingleApi(BaseCase):
    """
    我的购彩记录（单买）
    """
    union_id = settings.TEST_UNION_ID
    user_id = settings.TEST_USER_ID
    stock_id = 1


    def setUp(self):
        MysqlHelper().fix_user_money(balance=100000, user_id=self.user_id)

    def test_info_my_single_all(self):
        """
        查看用户单独购彩的购彩记录--全部数据
        :return:
        """
        # 调投注接口,代购3张
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 3, "buyType": 0, "window": 0, "roomId": 1, "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), "下单成功")

        info_my_single = InfoMySingleLotApi(self.union_id)
        info_my_single.get({'unionId': self.union_id, 'source': 1, 'detailStatus': None,
                            'bonusStatus': None, 'page': 1, 'length': 20})
        self.assertEqual(info_my_single.get_resp_code(),200)
        result = info_my_single.get_resp_result()
        self.assertEqual(len(result), 3)
        order_id = []
        for i in range(len(result)):
            order_id.append(result[i]['orderId'])

        all_list = MysqlHelper().get_order_details(order_id[0])
        self.assertEqual(result[0]["seq"], all_list["seq"])
        self.assertEqual(result[0]["detailStatus"], all_list["detail_status"])
        self.assertEqual(result[0]["amount"], all_list["amount"])
        self.assertEqual(result[0]["bonusStatus"], all_list["bonus_status"])
        self.assertEqual(result[0]["bonusAmount"], all_list["bonus_amount"])
        self.assertEqual(result[0]["bonusTime"], all_list["bonus_time"])
        self.assertEqual(result[0]["ticketNo"], all_list["ticket_no"])
        self.assertEqual(result[0]["route"], all_list["route"])
        self.assertEqual(result[0]["gpyId"], all_list["gpy_id"])
        self.assertEqual(result[0]["stationNumber"], all_list["station_number"])
        createTime = base_helper.get_nums_in_string(str(result[0]["createTime"]))
        create_time = base_helper.get_nums_in_string(str(all_list["create_time"]))
        self.assertEqual(createTime,create_time)

        for i in order_id:
            MysqlHelper().delete_order_details(i)

    def test_info_my_single_xiadan(self):
        """
        查看用户单独购彩的购彩记录--下单
        :return:
        """
        # 调投注接口,代购3张
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 3, "buyType": 0, "window": 0, "roomId": 1, "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), "下单成功")

        info_my_single = InfoMySingleLotApi(self.union_id)
        info_my_single.get({'unionId': self.union_id, 'source': 1, 'detailStatus': None,
                            'bonusStatus': None, 'page': 1, 'length': 20})
        self.assertEqual(info_my_single.get_resp_code(),200)
        result = info_my_single.get_resp_result()
        self.assertEqual(len(result), 3)
        order_id = []
        for i in range(len(result)):
            order_id.append(result[i]['orderId'])

        for i in range(len(result)):
            self.assertEqual(result[i]["detailStatus"],0)

        for i in order_id:
            MysqlHelper().delete_order_details(i)

    def tearDown(self):
        mysql = MysqlHelper()
        mysql.delete_lot_order(self.user_id)
        Redis().fix_stock_day_cache(stock_id=self.stock_id, num=10000)
        mysql.fix_user_money(balance=100000, user_id=self.user_id)
        mysql.delete_account_details(self.user_id)
        time.sleep(2)