# -*- coding:utf-8 -*-

from base_api.get_info_user import GetInfoUserApi
from base.base_case import BaseCase
from utilities.mysql_helper import MysqlHelper
import time, re


class TestGetInfoUserApi(BaseCase):
    """
    获取用户信息
    """

    def test_get_info_user(self):
        """
        成功获取信息
        :return:
        """
        info_user = GetInfoUserApi()
        info_user.get({"unionId": "4567", "source": "1"})
        self.assertEqual(info_user.get_resp_code(), 200)
        self.assertEqual(info_user.get_resp_message(), "success")
        result = info_user.get_resp_result()
        id = result["id"]
        user_info = MysqlHelper().get_lot_user_info(id)
        self.assertEqual(result["id"], user_info["id"])
        self.assertEqual(result["userName"], user_info["user_name"])
        self.assertEqual(result["password"], user_info["password"])
        self.assertEqual(result["email"], user_info["email"])
        self.assertEqual(result["userStatus"], user_info["user_status"])
        self.assertEqual(result["unionId"], user_info["union_id"])
        self.assertEqual(result["nickname"], user_info["nickname"])
        self.assertEqual(result["headPic"], user_info["head_pic"])
        self.assertEqual(result["platformId"], user_info["platform_id"])
        self.assertEqual(result["authId"], user_info["auth_id"])
        createTime = float(result["createTime"] / 1000)
        create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(createTime))
        num = re.compile(r'\d+')
        createTime = num.findall(create_time)
        create_time = num.findall(str(user_info["create_time"]))
        self.assertEqual(createTime, create_time)
        updateTime = float(result["updateTime"] / 1000)
        update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(updateTime))
        num = re.compile(r'\d+')
        updateTime = num.findall(update_time)
        update_time = num.findall(str(user_info["update_time"]))
        self.assertEqual(updateTime, update_time)

    def test_get_info_user_unionId_none(self):
        """
        unionId为空时
        :return:
        """
        info_user = GetInfoUserApi()
        info_user.get({"unionId": None, "source": "1"})
        self.assertEqual(info_user.get_resp_code(), 405)
        self.assertEqual(info_user.get_resp_message(), "fail")

    def test_get_info_user_source_none(self):
        """
        unionId为空时
        :return:
        """
        info_user = GetInfoUserApi()
        info_user.get({"unionId": "4567", "source": None})
        self.assertEqual(info_user.get_resp_code(), 405)
        self.assertEqual(info_user.get_resp_message(), "failed")
