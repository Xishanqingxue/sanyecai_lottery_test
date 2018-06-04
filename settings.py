# -*- coding:utf-8 -*-
import os
import time

ENV = 'test'

SKIP_REASON = '空参问题暂不修改，跳过测试'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SETTING_LOCAL = os.path.join(BASE_DIR, "settings_local.py")
if os.path.exists(SETTING_LOCAL):
    with open(SETTING_LOCAL, 'r') as f:
        exec(f.read())

API_TEST_BASE_URL = 'http://111.200.217.42:8386/video-lottery-base_api'

# 请求HEADERS配置
API_HEADERS = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8'}
AJAX_HEADERS = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'X-Requested-With': 'XMLHttpRequest'}

# 日志配置
now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
LOG_DIR_PATH = os.path.join(BASE_DIR,'log')
if not os.path.exists(LOG_DIR_PATH):
    os.mkdir('./log')
LOG_FILE_NAME = './log/{0}_log.txt'.format(now_time)
LOG_FORMATTER = "%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s"

# 测试报告配置
REPORT_DIR_PATH = os.path.join(BASE_DIR,'result')
if not os.path.exists(REPORT_DIR_PATH):
    os.mkdir('./result')
REPORT_FILE_NAME = './result/' + time.strftime("%Y%m%d%H%M%S") + '_result.html'
REPORT_TITLE = '吉刮彩接口自动化测试报告'
REPORT_DESCRIPTION = '用例执行情况详情如下:'
REPORT_TESTER = '吉刮彩测试人员'

# 邮件配置
MAIL_SERVER = 'smtp.163.com'
MAIL_FROM = '13501077762@163.com'
MAIL_FROM_PASSWORD = 'yinglong123'
MAIL_HEADER = '吉刮彩接口测试执行完成'
MAIL_TO = 'zhangmin@wozhongla.com' # 网媒测试
# MAIL_TO = 'liulei@kong.net'

# Mysql配置
TEST_MYSQL_CONFIG = {'host': '192.168.0.224', 'port': 3306, 'user': 'root', 'password': '111111'}
TEST_DEFAULT_DB = 'video_lottery'

# Redis配置
REDIS_CONFIG = {'host': '192.168.0.252', 'port': 6379}

# 测试账户配置
TEST_UNION_ID = 'dw_22608451'
TEST_USER_ID = '123'
TEST_USER_NAME = "ZBJKCdw_22608451"
TEST_NICKNAME = '秋阳丶'
TEST_HEAD_PIC = 'https://pic.dawang.tv/files/images/heads/2a/22/20170705213141666.jpeg'
# TEST_UNION_ID = 'dw_22017190'
# TEST_USER_ID = '285'
# TEST_USER_NAME = "ZBJKCdw_22017190"
# TEST_NICKNAME = '渔夫垂钓翁'
# TEST_HEAD_PIC = 'https://pic.t.dwtv.tv/files/images/heads/c8/cf/20180320144540859.jpg'
TEST_SOURCE = 1
