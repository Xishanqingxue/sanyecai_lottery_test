# -*- coding:utf-8 -*-
from base_api.bet_api import BetBetApi, BetBetApiNotLogin
from base.base_case import BaseCase
from base_api.my_join_api import MyJoinApi
from utilities.redis_helper import Redis
from utilities.mysql_helper import MysqlHelper
from base_api.my_ac_det_api import MyAcDetApi
import time,json
import settings


class TestBetGetSellLottApi(BaseCase):
    """
    下单投注接口(单买、合买)/我的合买记录列表/账户变动记录
    """
    union_id = settings.TEST_UNION_ID
    user_id = MysqlHelper().get_user_details(union_id)['id']
    stock_id = 1
    room_id = 1
    not_authentication_union_id = 8887

    def setUp(self):
        MysqlHelper().fix_user_money(balance=10000, user_id=self.user_id)

    def test_bet_not_authentication(self):
        """
        测试购买未进行实名认证
        :return:
        """
        bet_api = BetBetApi(self.not_authentication_union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 0, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 417)
        self.assertEqual(bet_api.get_resp_message(), u"没实名认证的用户，不能下单")

    def test_bet_one_success(self):
        """
        成功购买1注
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 0, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 1)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 0)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 1)
        self.assertEqual(order_list['amount'], 20.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(),u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result),1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'],self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'],1)
        self.assertEqual(result[0]['amount'],-20.0)
        self.assertEqual(result[0]['balance'],9980.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'],2)
        self.assertIsNone(result[0]['bak'])


    def test_bet_30_success(self):
        """
        成功代购30注
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 30, "buyType": 0, "window": 0, "roomId": self.room_id,
                     "shareMethod": None, "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 30)

        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 0)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 30)
        self.assertEqual(order_list['amount'], 600.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -600.0)
        self.assertEqual(result[0]['balance'], 9400.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_100_success(self):
        """
        成功代购100注
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 100, "buyType": 0, "window": 0, "roomId": self.room_id,
             "shareMethod": None, "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 100)

        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 0)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 100)
        self.assertEqual(order_list['amount'], 2000.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -2000.0)
        self.assertEqual(result[0]['balance'], 8000.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_50_success(self):
        """
        成功代购50注
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 50, "buyType": 0, "window": 0, "roomId": self.room_id,
             "shareMethod": None, "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 50)

        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 0)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 50)
        self.assertEqual(order_list['amount'], 1000.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -1000.0)
        self.assertEqual(result[0]['balance'], 9000.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_low_stocks(self):
        """
        测试库存不足情况下代购30张
        :return:
        """
        Redis().fix_stock_day_cache(stock_id=self.stock_id, num=10)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 30, "buyType": 0, "window": 0, "roomId": self.room_id,
                     "shareMethod": None, "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 410)
        self.assertEqual(bet_api.get_resp_message(), u"库存不足")

    def test_bet_low_money(self):
        """
        测试余额不足情况下代购30张
        :return:
        """
        MysqlHelper().fix_user_money(balance=10, user_id=self.user_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 30, "buyType": 0, "window": 0, "roomId": self.room_id,
                     "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 408)
        self.assertEqual(bet_api.get_resp_message(), u"余额不足")

    def test_bet_not_login(self):
        """
        测试未登录情况下代购
        :return:
        """
        bet_api = BetBetApiNotLogin()
        bet_api.get({"lotoId": self.stock_id, "nums": 30, "buyType": 0, "window": 0, "roomId": self.room_id,
                     "shareMethod": None,"memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 300)
        self.assertEqual(bet_api.get_resp_message(), u"未登录")

    def test_bet_specified_window(self):
        """
        测试代购指定窗口
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 2, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 1)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 0)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 1)
        self.assertEqual(order_list['amount'], 25.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 2)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -25.0)
        self.assertEqual(result[0]['balance'], 9975.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_regional_discrepancy(self):
        """
        测试北京用户不能购买彩票
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 2, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': 11})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"地域不符")

    def test_bet_loto_id_null(self):
        """
        测试请求接口彩种id为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": None, "nums": 1, "buyType": 0, "window": 2, "roomId": self.room_id, "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"无此彩种")

    def test_bet_loto_id_error(self):
        """
        测试请求接口彩种id不存在
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 9999, "nums": 1, "buyType": 0, "window": 2, "roomId": self.room_id, "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"无此彩种")

    def test_bet_nums_null(self):
        """
        测试请求购买数量为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": None, "buyType": 0, "window": 2, "roomId": 1, "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"购买张数必须大于零")

    def test_bet_buy_type_null(self):
        """
        测试请求接口购买类型为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 1, "buyType": None, "window": 2, "roomId": 1, "shareMethod": None,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"不支持的购买方式")

    def test_bet_room_id_null(self):
        """
        测试请求接口房间ID为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": None, "roomId": None, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"房间不能为空")

    def test_bet_window_null(self):
        """
        测试请求接口窗口为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": None, "roomId": self.room_id,
                     "shareMethod": None, "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")

    def test_bet_share_method_null(self):
        """
        测试请求接口合买类型为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 15, "buyType": 1, "window": None, "roomId": 1, "shareMethod": None,
             "memberNum": 2, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"分配方式不能为空")

    def test_bet_member_num_null(self):
        """
        测试请求接口合买人数为空
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": self.stock_id, "nums": 15, "buyType": 1, "window": None, "roomId": 1, "shareMethod": 0,
                     "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买人数不能为空")

    def test_bet_2_max_win(self):
        """
        测试2人合买多者全拿
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
                     "memberNum": 2, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 2)
        self.assertEqual(result[0]['share'], 0)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_2_max_win_amount_not_300(self):
        """
        测试2人合买多者全拿,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
                     "memberNum": 2, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_2_mix_win(self):
        """
        测试2人合买少者全拿
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 2,
                     "memberNum": 2, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 2)
        self.assertEqual(result[0]['share'], 2)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_2_min_win_amount_not_300(self):
        """
        测试2人合买少者全拿,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 2,
                     "memberNum": 2, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_2_average(self):
        """
        测试2人合买奖金均分
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 1,
                     "memberNum": 2, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 2)
        self.assertEqual(result[0]['share'], 1)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_2_average_amount_not_300(self):
        """
        测试2人合买奖金均分,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 1,
                     "memberNum": 2, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_5_max_win(self):
        """
        测试5人合买多者全拿
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
                     "memberNum": 5, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 5)
        self.assertEqual(result[0]['share'], 0)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_5_max_win_amount_not_300(self):
        """
        测试5人合买多者全拿,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
                     "memberNum": 5, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_5_mix_win(self):
        """
        测试5人合买少者全拿
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 2,
                     "memberNum": 5, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 5)
        self.assertEqual(result[0]['share'], 2)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_5_min_win_amount_not_300(self):
        """
        测试5人合买少者全拿,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 2,
                     "memberNum": 5, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_5_average(self):
        """
        测试5人合买奖金均分
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 1,
                     "memberNum": 5, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 5)
        self.assertEqual(result[0]['share'], 1)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_5_average_amount_not_300(self):
        """
        测试5人合买奖金均分,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 1,
                     "memberNum": 5, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_9_max_win(self):
        """
        测试9人合买多者全拿
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
                     "memberNum": 9, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 9)
        self.assertEqual(result[0]['share'], 0)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_9_max_win_amount_not_300(self):
        """
        测试9人合买多者全拿,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 0,
                     "memberNum": 9,
                     'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_9_mix_win(self):
        """
        测试9人合买少者全拿
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 2,
                     "memberNum": 9, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 9)
        self.assertEqual(result[0]['share'], 2)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_9_min_win_amount_not_300(self):
        """
        测试9人合买少者全拿,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 2,
                     "memberNum": 9,
                     'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_9_average(self):
        """
        测试9人合买奖金均分
        :return:
        """
        bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 15, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 1,
                     "memberNum": 9, 'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        after_bet_numbers = Redis().get_stock_day_cache(stock_id=self.stock_id)
        self.assertEqual(int(bet_numbers) - int(after_bet_numbers), 15)
        # 校验没有拆单
        order_list = MysqlHelper().get_lot_order(self.user_id)[0]
        self.assertEqual(len(order_list), 22)
        self.assertNotEqual(len(order_list['order_no']), 0)
        self.assertEqual(int(order_list['lottery_id']), self.stock_id)
        self.assertEqual(order_list['buy_type'], 1)
        self.assertEqual(order_list['order_status'], 0)
        self.assertIsNone(order_list['bonus_status'], 0)
        self.assertIsNone(order_list['station_num'], 0)
        self.assertEqual(order_list['num'], 15)
        self.assertEqual(order_list['amount'], 300.00)
        self.assertEqual(order_list['source'], 1)
        self.assertEqual(order_list['room_id'], 1)
        self.assertEqual(order_list['window'], 0)
        self.assertIsNone(order_list['back_amount'])
        self.assertIsNone(order_list['bonus_amount'])
        self.assertIsNone(order_list['actual_bonus'])
        self.assertIsNotNone(order_list['project_id'])
        self.assertIsNone(order_list['refund'])
        self.assertIsNone(order_list['bonus'])
        self.assertIsNone(order_list['bak'])

        # 我的合买记录
        my_join_api = MyJoinApi(self.union_id)
        my_join_api.get({'status': None, 'page': 1, 'length': 10})

        self.assertEqual(my_join_api.get_resp_code(), 200)
        self.assertEqual(my_join_api.get_resp_message(), u'success')

        result = my_join_api.get_resp_result()

        self.assertEqual(len(result), 1)
        self.assertIsNotNone(result[0]['projectNo'])
        self.assertEqual(result[0]['memberNum'], 9)
        self.assertEqual(result[0]['share'], 1)
        self.assertEqual(result[0]['projectStatus'], 0)
        self.assertIsNone(result[0]['bonusSum'])
        self.assertIsNone(result[0]['userId'])
        self.assertIsNotNone(result[0]['roomId'])
        self.assertIsNotNone(result[0]['projectNo'])

        # 账户变动记录
        my_ac_det_api = MyAcDetApi(self.union_id)
        my_ac_det_api.get({'unionId': self.union_id, 'source': 1})

        self.assertEqual(my_ac_det_api.get_resp_code(), 200)
        self.assertEqual(my_ac_det_api.get_resp_message(), u'success')

        result = my_ac_det_api.get_resp_result()
        self.assertEqual(len(result), 1)

        self.assertIsNotNone(result[0]['serialNo'])
        self.assertEqual(result[0]['userId'], self.user_id)
        self.assertIsNotNone(result[0]['accountNo'])
        self.assertEqual(result[0]['accountType'], 1)
        self.assertEqual(result[0]['amount'], -300.0)
        self.assertEqual(result[0]['balance'], 9700.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 2)
        self.assertIsNone(result[0]['bak'])

    def test_bet_9_average_amount_not_300(self):
        """
        测试9人合买奖金均分,金额不足300
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get({"lotoId": 1, "nums": 10, "buyType": 1, "window": 0, "roomId": self.room_id, "shareMethod": 1,
                     "memberNum": 9,
                     'provinceId': 1})
        self.assertEqual(bet_api.get_resp_code(), 401)
        self.assertEqual(bet_api.get_resp_message(), u"合买金额必须为300")

    def test_bet_be_fast(self):
        """
        测试禁止下单过快
        :return:
        """
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 0, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 200)
        self.assertEqual(bet_api.get_resp_message(), u"下单成功")
        bet_api = BetBetApi(self.union_id)
        bet_api.get(
            {"lotoId": self.stock_id, "nums": 1, "buyType": 0, "window": 0, "roomId": self.room_id, "shareMethod": None,
             "memberNum": None, 'provinceId': None})
        self.assertEqual(bet_api.get_resp_code(), 411)
        self.assertEqual(bet_api.get_resp_message(), u"下单过快")

    def tearDown(self):
        mysql = MysqlHelper()
        mysql.delete_lot_order(self.user_id)
        Redis().fix_stock_day_cache(stock_id=self.stock_id, num=10000)
        mysql.fix_user_money(balance=0, user_id=self.user_id)
        mysql.delete_account_details(self.user_id)
        time.sleep(2)
