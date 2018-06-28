#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/28 14:09
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : test_1.py
# @Software: PyCharm
import unittest
class ud(unittest.TestCase):
    def setUp(self):
        pass
    def tearDown(self):
        pass
    def test_01(self):
        print ("01")
    def test_02(self):
        print ("02")
if __name__ == '__main__':
    unittest.main()