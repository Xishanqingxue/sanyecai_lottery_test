# -*- coding:utf-8 -*-
from base_api.login_api import LoginApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlHelper
import settings


class TestLoginApi(BaseCase):
    """
    登录
    """
    union_id = settings.TEST_UNION_ID
    new_union_id = '8888'

    # @classmethod
    # def setUpClass(cls):
    #     MysqlHelper().delete_user(union_id=cls.new_union_id)

    def test_login_success(self):
        """
        测试登录成功
        """
        login_api = LoginApi()
        login_api.login(unionID=self.union_id)

        self.assertEqual(login_api.get_resp_code(), 200)
        self.assertEqual(login_api.get_resp_message(), u'success')

        user_details = MysqlHelper().get_user_details(self.union_id)
        result = login_api.get_resp_result()
        self.assertEqual(result['id'], user_details['id'])
        self.assertEqual(result['userName'], user_details['user_name'])
        self.assertEqual(result['userStatus'], user_details['user_status'])
        self.assertEqual(result['unionId'], self.union_id)
        self.assertEqual(result['nickname'], user_details['nickname'])
        self.assertEqual(result['headPic'], user_details['head_pic'])
        self.assertEqual(result['platformId'], user_details['platform_id'])
        self.assertEqual(result['authId'], user_details['auth_id'])

    def test_login_union_id_null(self):
        """
        测试请求登录接口union_id为空
        """
        login_api = LoginApi()
        login_api.login(unionID=None)

        self.assertEqual(login_api.get_resp_code(), 301)
        self.assertEqual(login_api.get_resp_message(), u'the sign failed')

    def test_login_source_null(self):
        """
        测试请求登录接口source为空
        """
        login_api = LoginApi()
        login_api.login(unionID=self.union_id, source=None)

        self.assertEqual(login_api.get_resp_code(), 301)
        self.assertEqual(login_api.get_resp_message(), u'the sign failed')

    def test_login_nickname_null(self):
        """
        测试请求登录接口nickname为空
        """
        login_api = LoginApi()
        login_api.login(unionID=self.union_id, nickname=None)

        self.assertEqual(login_api.get_resp_code(), 301)
        self.assertEqual(login_api.get_resp_message(), u'the sign failed')

    def test_login_head_pic_null(self):
        """
        测试请求登录接口head_pic为空
        """
        login_api = LoginApi()
        login_api.login(unionID=self.union_id, head_pic=None)

        self.assertEqual(login_api.get_resp_code(), 301)
        self.assertEqual(login_api.get_resp_message(), u'the sign failed')

    def test_login_sign_null(self):
        """
        测试请求登录接口sign为空
        """
        login_api = LoginApi()
        login_api.login(unionID=self.union_id, sign_is_null=True)

        self.assertEqual(login_api.get_resp_code(), 301)
        self.assertEqual(login_api.get_resp_message(), u'the sign failed')

    def test_first_login_register(self):
        """
        测试首次登录数据库信息
        """
        nickname = 'Auto_Test'
        head_pic = '/pic/head_pic_0016.jpg'
        login_api = LoginApi()
        login_api.login(unionID=self.new_union_id, source=2, nickname=nickname, head_pic=head_pic)

        self.assertEqual(login_api.get_resp_code(), 200)
        self.assertEqual(login_api.get_resp_message(), u'success')

        user_details = MysqlHelper().get_user_details(self.new_union_id)
        result = login_api.get_resp_result()
        self.assertEqual(result['id'], user_details['id'])
        self.assertEqual(result['userName'], user_details['user_name'])
        self.assertEqual(result['userStatus'], user_details['user_status'])
        self.assertEqual(result['unionId'], self.new_union_id)
        self.assertEqual(result['nickname'], user_details['nickname'])
        self.assertEqual(result['headPic'], user_details['head_pic'])
        self.assertEqual(result['platformId'], user_details['platform_id'])
        self.assertEqual(result['authId'], user_details['auth_id'])

    @classmethod
    def tearDownClass(cls):
        MysqlHelper().delete_user(union_id=cls.new_union_id)
