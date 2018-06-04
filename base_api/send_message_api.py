# # -*- coding:utf-8 -*-
# from base.login_base_api import LoginBaseApi
#
# class SendMessageApi(LoginBaseApi):
#     """
#     发送短信验证码
#     """
#     url = "/finan/sendMessage"
#
#     def build_custom_param(self, data):
#         return {'mobile':data['mobile'],'type':data['type'],'imgCode':data['imgCode']}