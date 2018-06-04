# -*- coding:utf-8 -*-
from base_api.withdraw_apply_api import WithdrawApplyApi
from base_api.image_code_api import ImageCodeApi
from base_api.send_sms_message_api import SendSmsMessageApi
from base_api.my_ac_det_api import MyAcDetApi
from base_api.my_precent_api import MyPrecentApi
from utilities.redis_helper import Redis
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlHelper
import json


class TestWithDrawApplyApi(BaseCase):
    """
    申请提现
    """
    union_id = '8880'
    mobile = '13511128945'
    user_id = MysqlHelper().get_user_details(union_id)['id']
    auth_id = 51

    def test_withdraw_apply_amount_less(self):
        """
        测试账户剩余提现额度不足时申请提现
        :return:
        """
        image_code_api = ImageCodeApi()
        image_code_api.get({'mobile': self.mobile})

        image_code = Redis().get_image_code(self.mobile)
        sms_code_api = SendSmsMessageApi(self.union_id,nickname='real_name12',head_pic='/pic/head_pic_16.jpg')
        response = sms_code_api.get({'mobile': self.mobile, 'type': 'tx_sms_code', 'imgCode': image_code})
        print(json.loads(response.text))

        sms_code = Redis().get_sms_code(self.mobile, type='tx')

        withdraw_api = WithdrawApplyApi(self.union_id,nickname='real_name12',head_pic='/pic/head_pic_16.jpg')
        withdraw_api.get({'amount': 500, 'source': 1, 'mobile':self.mobile ,
                'verCode': sms_code, 'type': 'tx_sms_code','bindingId':2})
        self.assertEqual(withdraw_api.get_resp_code(),422)
        self.assertEqual(withdraw_api.get_resp_message(),u'账户剩余提现额度不足,请查看后重试!')

    def test_withdraw_mobile_error(self):
        """
        测试提现手机号与绑定手机号不一致时申请提现
        :return:
        """
        withdraw_api = WithdrawApplyApi(self.union_id, nickname='real_name12', head_pic='/pic/head_pic_16.jpg')
        withdraw_api.get({'amount': 500, 'source': 1, 'mobile': '13288888888',
                          'verCode': '1233', 'type': 'tx_sms_code', 'bindingId': 2})
        self.assertEqual(withdraw_api.get_resp_code(), 414)
        self.assertEqual(withdraw_api.get_resp_message(), u'手机号码错误,请使用尾号: 8945的手机号进行验证!')

    def test_withdraw_apply_amount_less_than_10(self):
        """
        测试当天首次提现成功
        :return:
        """
        Redis().fix_user_withdraw_times(self.auth_id,0)
        MysqlHelper().fix_user_money(balance=100, user_id=self.user_id)
        MysqlHelper().fix_user_withdraw_amount(auth_id=self.auth_id,amount=100)
        image_code_api = ImageCodeApi()
        image_code_api.get({'mobile': self.mobile})

        image_code = Redis().get_image_code(self.mobile)
        sms_code_api = SendSmsMessageApi(self.union_id,nickname='real_name12',head_pic='/pic/head_pic_16.jpg')
        sms_code_api.get({'mobile': self.mobile, 'type': 'tx_sms_code', 'imgCode': image_code})

        sms_code = Redis().get_sms_code(self.mobile, type='tx')

        withdraw_api = WithdrawApplyApi(self.union_id,nickname='real_name12',head_pic='/pic/head_pic_16.jpg')
        withdraw_api.get({'amount': 100, 'source': 1, 'mobile':self.mobile ,
                'verCode': sms_code, 'type': 'tx_sms_code','bindingId':2})
        self.assertEqual(withdraw_api.get_resp_code(),200)
        self.assertEqual(withdraw_api.get_resp_message(),u'提现申请成功,请等待管理员审核!')

        # 提现记录
        my_precent_api = MyPrecentApi(self.union_id)
        my_precent_api.get({'page': None, 'length': None})

        self.assertEqual(my_precent_api.get_resp_code(),200)
        self.assertEqual(my_precent_api.get_resp_message(),u'success')

        result = my_precent_api.get_resp_result()
        self.assertEqual(len(result),1)
        self.assertIsNotNone(result[0]['presentRecordNo'])
        self.assertEqual(result[0]['authId'],self.auth_id)
        self.assertEqual(result[0]['amount'],100.0)
        self.assertEqual(result[0]['actualAmount'],100.0)
        self.assertIsNone(result[0]['amountOfCash'])
        self.assertEqual(result[0]['tip'],0.0)
        self.assertEqual(result[0]['presentRecordStatus'],0)
        self.assertIsNone(result[0]['presentRecordStatusPre'])
        self.assertEqual(result[0]['debitStatus'], u'1')
        self.assertEqual(result[0]['source'], 1)
        self.assertEqual(result[0]['notify'], 9)
        self.assertIsNone(result[0]['bak'])
        self.assertEqual(result[0]['realName'], u'林华')
        self.assertEqual(result[0]['mobile'], self.mobile)
        self.assertEqual(result[0]['bindingId'],2)

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
        self.assertEqual(result[0]['amount'], -100.0)
        self.assertEqual(result[0]['balance'], 0.0)
        self.assertEqual(result[0]['oppoUserid'], 88)
        self.assertEqual(result[0]['oppoAccountNo'], 881)
        self.assertIsNotNone(result[0]['orderNo'])
        self.assertEqual(result[0]['tradeType'], 3)
        self.assertIsNone(result[0]['bak'])

    def test_withdraw_apply_amount_max_than_5000(self):
        """
        测试当天提现金额已达5000后申请提现失败
        :return:
        """
        Redis().fix_user_withdraw_times(self.auth_id,1)
        Redis().fix_user_withdraw_money_today(self.auth_id,5000)
        MysqlHelper().fix_user_money(balance=100, user_id=self.user_id)
        MysqlHelper().fix_user_withdraw_amount(auth_id=self.auth_id,amount=100)
        image_code_api = ImageCodeApi()
        image_code_api.get({'mobile': self.mobile})

        image_code = Redis().get_image_code(self.mobile)
        sms_code_api = SendSmsMessageApi(self.union_id,nickname='real_name12',head_pic='/pic/head_pic_16.jpg')
        sms_code_api.get({'mobile': self.mobile, 'type': 'tx_sms_code', 'imgCode': image_code})

        sms_code = Redis().get_sms_code(self.mobile, type='tx')

        withdraw_api = WithdrawApplyApi(self.union_id,nickname='real_name12',head_pic='/pic/head_pic_16.jpg')
        withdraw_api.get({'amount': 100, 'source': 1, 'mobile':self.mobile ,
                'verCode': sms_code, 'type': 'tx_sms_code','bindingId':2})
        self.assertEqual(withdraw_api.get_resp_code(),423)
        self.assertEqual(withdraw_api.get_resp_message(),u'当天剩余提现额度不足,请明日重试!')

    def tearDown(self):
        MysqlHelper().fix_user_withdraw_amount(auth_id=self.auth_id,amount=0)
        MysqlHelper().delete_user_withdraw_log(auth_id=self.auth_id)
        MysqlHelper().delete_account_details(self.user_id)
        Redis().fix_user_withdraw_times(self.auth_id, 0)
        Redis().fix_user_withdraw_money_today(self.auth_id, 0)
