# # -*- coding:utf-8 -*-
# from base.login_base_api import LoginBaseApi
# from base.base_api import BaseApi
#
# class BetApi(LoginBaseApi):
#     """
#     购彩下订单
#     """
#     url = "/bet/bet"
#
#     def build_custom_param(self, data):
#         return {'lotoId':data['lotoId'],'nums':data['nums'],'buyType':data['buyType'],
#                 'window':data['window'],'roomId':data['roomId'],'shareMethod':data['shareMethod'],
#                 'memberNum':data['memberNum'],'provinceId':data['provinceId']}
#
# # class BetBetApiNotLogin(BaseApi):
#     # """
#     # 投注(未登录)
#     # """
#     # url = "/video-lottery-base_api/bet/bet"
#     #
#     # def build_custom_param(self, data):
#     #     return {'lotoId':data['lotoId'],'nums':data['nums'],'buyType':data['buyType'],
#     #             'window':data['window'],'roomId':data['roomId'],'shareMethod':data['shareMethod'],
#     #             'memberNum':data['memberNum'],'provinceId':data['provinceId']}