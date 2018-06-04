# -*- coding:utf-8 -*-
from base_api.send_sms_message_api import SendSmsMessageApi
from base_api.image_code_api import ImageCodeApi
from base_api.edit_mobile_api import EditMobileApi
from utilities.mysql_helper import MysqlHelper as mysql
from base.base_case import BaseCase
from utilities.redis_helper import Redis
import random
import settings
import json
import unittest


class TestEditMobileApi(BaseCase):
    """
    修改绑定手机号
    """
    union_id = settings.TEST_UNION_ID
    auth_id = mysql().get_user_details(union_id)['auth_id']
    new_mobile = '1581111' + str(random.randint(2222,9999))
    old_mobile = '13511114758'

    def test_edit_mobile_success(self):
        """
        测试修改绑定手机号成功
        :return:
        """
        # 验证原手机号
        image_code_api = ImageCodeApi()
        image_code_api.get({'mobile': self.old_mobile})

        image_code = Redis().get_image_code(self.old_mobile)
        sms_code_api = SendSmsMessageApi(self.union_id)
        sms_code_api.get({'mobile': self.old_mobile, 'type': 'xg_sms_code', 'imgCode': image_code})
        # self.assertEqual(sms_code_api.get_resp_code(), 200)
        sms_code = Redis().get_sms_code(self.old_mobile, type='xg')

        edit_mobile_api = EditMobileApi(self.union_id)
        edit_mobile_api.get({'mobile':self.old_mobile,'verCode':sms_code,'type':'xg_sms_code'})

        # self.assertEqual(edit_mobile_api.get_resp_code(),200)

        # 绑定新手机号
        image_code_api = ImageCodeApi()
        image_code_api.get({'mobile': self.new_mobile})

        image_code = Redis().get_image_code(self.new_mobile)
        sms_code_api = SendSmsMessageApi(self.union_id)
        sms_code_api.get({'mobile': self.new_mobile, 'type': 'xg_sms_code', 'imgCode': image_code})

        # self.assertEqual(sms_code_api.get_resp_code(), 200)
        sms_code = Redis().get_sms_code(self.new_mobile, type='xg')

        edit_mobile_api = EditMobileApi(self.union_id)
        edit_mobile_api.get({'mobile': self.new_mobile, 'verCode': sms_code, 'type': 'xg_sms_code'})

        self.assertEqual(edit_mobile_api.get_resp_code(), 200)

        self.assertEqual(self.new_mobile,mysql().get_user_auth(self.auth_id)['mobile'])

    def test_edit_mobile_old_mobile_error(self):
        """
        测试请求接口原手机号错误
        :return:
        """
        image_code_api = ImageCodeApi()
        image_code_api.get({'mobile': self.new_mobile})

        image_code = Redis().get_image_code(self.new_mobile)
        sms_code_api = SendSmsMessageApi(self.union_id)
        sms_code_api.get({'mobile': self.new_mobile, 'type': 'xg_sms_code', 'imgCode': image_code})

        self.assertEqual(sms_code_api.get_resp_code(), 200)
        sms_code = Redis().get_sms_code(self.new_mobile, type='xg')

        edit_mobile_api = EditMobileApi(self.union_id)
        edit_mobile_api.get({'mobile':self.new_mobile,'verCode':sms_code,'type':'xg_sms_code'})

        self.assertEqual(edit_mobile_api.get_resp_code(),414)
        self.assertEqual(edit_mobile_api.get_resp_message(),u'原手机号错误,请重新填写!')

    @unittest.skip(reason=settings.SKIP_REASON)
    def test_edit_mobile_ver_code_null(self):
        """
        测试请求接口手机验证码为空
        :return:
        """
        edit_mobile_api = EditMobileApi(self.union_id)
        edit_mobile_api.get({'mobile':self.new_mobile,'verCode':None,'type':'xg_sms_code'})

        self.assertEqual(edit_mobile_api.get_resp_code(),414)
        self.assertEqual(edit_mobile_api.get_resp_message(),u'手机验证码错误,请重新填写!')

    @unittest.skip(reason=settings.SKIP_REASON)
    def test_edit_mobile_mobile_null(self):
        """
        测试请求接口手机号为空
        :return:
        """
        edit_mobile_api = EditMobileApi(self.union_id)
        edit_mobile_api.get({'mobile':None,'verCode':'1234','type':'xg_sms_code'})

        self.assertEqual(edit_mobile_api.get_resp_code(),413)
        self.assertEqual(edit_mobile_api.get_resp_message(),u'手机验证码错误,请重新填写!')

    @unittest.skip(reason=settings.SKIP_REASON)
    def test_edit_mobile_type_null(self):
        """
        测试请求接口手机验证码错误
        :return:
        """
        edit_mobile_api = EditMobileApi(self.union_id)
        edit_mobile_api.get({'mobile':self.new_mobile,'verCode':'1234','type':None})

        self.assertEqual(edit_mobile_api.get_resp_code(),413)
        self.assertEqual(edit_mobile_api.get_resp_message(),u'手机验证码错误,请重新填写!')

    def tearDown(self):
        mysql().fix_user_mobile(self.auth_id,mobile=self.old_mobile)
