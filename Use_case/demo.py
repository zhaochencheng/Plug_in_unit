#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 16:15
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : demo.py
# @Software: PyCharm
import unittest
import requests
from Plug_in_unit.public_script.function_public import *
from Plug_in_unit.Mongo_init.Mongo_Client import *
import logging as log
import time
log.basicConfig(level=log.DEBUG)

class demo(unittest.TestCase):
    url = get_data("sms_server", "url")
    def setUp(self):
        time.sleep(1)
        pass
    def tearDown(self):
        pass

    def test_01(self):
        SmsRecord = get_data("mongo_integration","collection1")
        SmsStatisticsForAppOfDay = get_data("mongo_integration","collection2")
        SmsStatisticsForAppOfMonth = get_data("mongo_integration","collection3")
        SmsStatisticsForChannelOfDay = get_data("mongo_integration","collection4")
        SmsStatisticsForChannelOfMonth = get_data("mongo_integration","collection5")
        SmsStatisticsForTidOfDay = get_data("mongo_integration","collection6")
        SmsStatisticsForTidOfMonth = get_data("mongo_integration","collection7")
        AppofDay_count_old = self.mongo_collection_count(SmsStatisticsForAppOfDay)
        print "APP每日发送总量",AppofDay_count_old
        AppofMonth_count_old = self.mongo_collection_count(SmsStatisticsForAppOfMonth)
        print "APP每月发送总量",AppofMonth_count_old
        ChannelOfDay_count_old = self.mongo_collection_count(SmsStatisticsForChannelOfDay)
        print "通道每日发送总量",ChannelOfDay_count_old
        ChannelOfMonth_count_old = self.mongo_collection_count(SmsStatisticsForChannelOfMonth)
        print "通道每月发送总量",ChannelOfMonth_count_old
        TidOfDay_count_old = self.mongo_collection_count(SmsStatisticsForTidOfDay)
        print "短信模板每日发送总量",TidOfDay_count_old
        TidOfMonth_count_old = self.mongo_collection_count(SmsStatisticsForTidOfMonth)
        print "短信模板每月发送总量",TidOfMonth_count_old

        # #
        # code_num = int(time.time())  #构建一个验证码；按时间构建保证唯一性 并和目前使用验证码不冲突
        # print "code_num：",code_num
        # #post 请求体 内容，并将验证码添加至请求体重
        # body_content = {"appid": "OD0QS8Z6","phone": ["18856361920"],"tid": "10202","tp": "{'msgcontent':''}"}
        # code_content= {'msgcontent':''}
        # code_content['msgcontent'] = code_num
        # body_content["tp"] = code_content
        # #向接口发送请求
        # r = requests.post(url=self.url,json=body_content)
        # print "接口返回信息：",r.content
        # #校验接口返回信息
        # self.assertEqual(r.content,'{"code":"000000","desc":"成功"}')
        #
        # '''#### 验证消息插件功能 #####'''
        # #构建查询条件
        # query_criteria = {"Content":""}
        # query_criteria["Content"] = "【科大讯飞】"+str(code_num)
        # self.mongo_Recordquery(query_criteria)




    def mongo_Recordquery(self,condition):
        #获取mongo信息 链接mongo
        host = get_data("mongo_integration","mongohost")
        port = int(get_data("mongo_integration","port"))
        database = get_data("mongo_integration","database")
        SmsRecord = get_data("mongo_integration","collection1")
        SmsStatisticsForAppOfDay = get_data("mongo_integration","collection2")
        SmsStatisticsForAppOfMonth = get_data("mongo_integration","collection3")
        SmsStatisticsForChannelOfDay = get_data("mongo_integration","collection4")
        SmsStatisticsForChannelOfMonth = get_data("mongo_integration","collection5")
        SmsStatisticsForTidOfDay = get_data("mongo_integration","collection6")
        SmsStatisticsForTidOfMonth = get_data("mongo_integration","collection7")

        data = Mongo().connect_mongo(host=host,port=port,database=database,collection=SmsRecord).find_one(condition)
        print "mongo历史记录表查询数据：",data
        status = data["Status"]
        Appid = data["Appid"]
        Tid = data["Tid"]
        Channel = data["Channel"]
        Sid = data["Sid"]
        print "短信状态：",status
        print "生成时间：",data["Stm"]
        print "Sid：",Sid
        print "Appid：",Appid
        print "模板ID：",Tid
        print "短信通道：",Channel
    def mongo_collection_count(self,collection):
        host = get_data("mongo_integration","mongohost")
        port = int(get_data("mongo_integration","port"))
        database = get_data("mongo_integration","database")
        data = Mongo().connect_mongo(host=host,port=port,database=database,collection=collection).count()
        return data




    # def test_02(self):
    #     code_num = int(time.time())  #构建一个验证码；按时间构建保证唯一性 并和目前使用验证码不冲突
    #     print "code_num",code_num
    #     #post 请求体 内容，并将验证码添加至请求体重
    #     body_content = {"appid": "OD0QS8Z6","phone": ["18856361920"],"tid": "10202","tp": "{'msgcontent':''}"}
    #     code_content= {'msgcontent':''}
    #     code_content['msgcontent'] = code_num
    #     body_content["tp"] = code_content
    #     #向接口发送请求
    #     r = requests.post(url=self.url,json=body_content)
    #     print "接口返回信息：",r.content
    #     #校验接口返回信息
    #     self.assertEqual(r.content,'{"code":"000000","desc":"成功"}')
    #     '''#### 验证消息插件功能 #####'''
    #     #获取mongo信息 链接mongo
    #     host = get_data("mongo_integration","mongohost")
    #     port = int(get_data("mongo_integration","port"))
    #     database = get_data("mongo_integration","database")
    #     collection = get_data("mongo_integration","collection")
    #     #构建查询条件
    #     query_criteria = {"Content":""}
    #     query_criteria["Content"] = "【科大讯飞】"+str(code_num)
    #     data = Mongo().connect_mongo(host=host,port=port,database=database,collection=collection).find_one(query_criteria)
    #     print data
    #     # print self.code_num



if __name__ == '__main__':
    unittest.main()