# -*- coding:utf-8 -*-
from unittest import TestCase
from base.base_log import BaseLogger
from base.base_helper import generate_random_nickname


logger = BaseLogger(__name__).get_logger()


class BaseCase(TestCase):
    union_id = ''