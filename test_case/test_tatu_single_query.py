# -*- coding:utf-8 -*-
from base_api.tabu_single_query_api import TatuSingleQuery
from base_api.bet_api import BetBetApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlHelper
import settings,time

class TestTatuSingleQuery(BaseCase):
    """
    单买购彩用户排队
    """
    union_id = 8880
    stock_id = 1
    room_id = 1
    user_id = 213
    def setUp(self):
        MysqlHelper().fix_user_money(balance=10000, user_id=self.user_id)

    def test_tatu_single_query(self):
        """
        单买购彩用户排队
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 0, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        time.sleep(1)

        single_query = TatuSingleQuery()
        single_query.get()
        self.assertEqual(single_query.get_resp_code(),200)
        self.assertEqual(single_query.get_resp_message(),"success")
        result = single_query.get_resp_result()
        # 获取用户的信息为列表前5？
        self.assertEqual(len(result),5)
        single_user_id_list = MysqlHelper().get_single_query_list()
        # 检验等待匹配列表中用户的昵称
        nickname = []
        for i in range(len(result)):
            nickname.append(result[i]["nickname"])
        mysql_nickname = MysqlHelper().get_user_info_nickname(single_user_id_list)
        for i in range(len(result)):
            self.assertEqual(nickname[i],mysql_nickname[i]["nickname"])

        # 校验等待匹配列表中用户的待开奖张数

    def tearDown(self):
        MysqlHelper().fix_user_money(balance=0, user_id=self.user_id)
        MysqlHelper().delete_lot_order(user_id=self.user_id)
        MysqlHelper().delete_order_detail_use_order_id(self.union_id)
