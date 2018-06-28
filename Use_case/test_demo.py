#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 16:15
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : test_demo.py
# @Software: PyCharm
import unittest
import requests
from Plug_in_unit.public_script.function_public import *
from Plug_in_unit.Mongo_init.Mongo_Client import *
from Plug_in_unit.Elasticsearch_init.elasticsearch_init import *
import logging as log
import time
log.basicConfig(level=log.DEBUG)

class Sms_consumer(unittest.TestCase):
    '''短信消息插件功能验证'''
    url = get_data("sms_server", "url")
    urlcallbacktencent = get_data("sms_server", "url_callbacktencent")
    def setUp(self):
        time.sleep(1)
        pass
    def tearDown(self):
        pass

    def test_01(self):
        ''' 验证consumer在mongo和ES数据存储一致 '''
        SmsRecord = get_data("mongo_integration","collection1")
        SmsStatisticsForAppOfDay = get_data("mongo_integration","collection2")
        SmsStatisticsForAppOfMonth = get_data("mongo_integration","collection3")
        SmsStatisticsForChannelOfDay = get_data("mongo_integration","collection4")
        SmsStatisticsForChannelOfMonth = get_data("mongo_integration","collection5")
        SmsStatisticsForTidOfDay = get_data("mongo_integration","collection6")
        SmsStatisticsForTidOfMonth = get_data("mongo_integration","collection7")

        ES_host = get_data("ES", "servers")
        ES_index = get_data("ES", "index")
        ES_query_total = get_data("ES", "query_total")

        yes_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # print yes_time

        smsrecordcount_old = self.mongo_collection_count(SmsRecord,{'Appid': '100IME'}).count()
        print("该appid短信发送总条数：",smsrecordcount_old)

        condition_forAPP = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP["StatisticsTime"] = yes_time
        condition_forAPPDay = condition_forAPP
        AppofDay_count_old = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay)
        print("APP每日短信量",AppofDay_count_old)
        condition_forAPP["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth = condition_forAPP
        AppofMonth_count_old = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth)
        print("APP每月短信量",AppofMonth_count_old)

        condition_forChannel = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel["StatisticsTime"] = yes_time
        condition_forChannelDay = condition_forChannel
        ChannelOfDay_count_old =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay)
        print("通道每日短信量",ChannelOfDay_count_old)
        condition_forChannel["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth = condition_forChannel
        ChannelOfMonth_count_old = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth)
        print("通道每月短信量",ChannelOfMonth_count_old)

        condition_forTid = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid["StatisticsTime"] = yes_time
        condition_forTidDay = condition_forTid
        TidOfDay_count_old = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay)
        print("短信模板每日短信量",TidOfDay_count_old)
        condition_forTid["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth = condition_forTid
        TidOfMonth_count_old = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth)
        print("短信模板每月短信量",TidOfMonth_count_old)


        resp_doc = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_old = resp_doc['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_old)

        #
        # # # #
        code_num = int(time.time())  # 构建一个验证码；按时间构建保证唯一性 并和目前使用验证码不冲突
        print("code_num：",code_num)
        # post 请求体 内容，并将验证码添加至请求体重
        body_content = {"appid": "100IME","phone": ["18856361920"],"tid": "10205","tp": "{'Code':'', 'Seq':'999', 'Minute':'50'}"}
        code_content= {'Code':'', 'Seq':'999', 'Minute':'50'}
        code_content['Code'] = code_num
        body_content["tp"] = code_content
        # 向接口发送请求
        r = requests.post(url=self.url,json=body_content)
        print("接口返回信息：",r.text)
        # 校验接口返回信息
        self.assertEqual(r.text,'{"code":"000000","desc":"成功"}')
        time.sleep(15)
        '''#### 验证消息插件功能 #####'''
        # 构建查询条件
        query_criteria = {"Content":""}
        query_criteria["Content"] = "【科大讯飞】您好，您本次操作的验证码为%s，序号为999。请在50分钟内使用，过期无效。" % str(code_num)
        record_data = self.mongo_Recordquery(query_criteria)
        print("mongo历史记录表查询数据：", record_data)
        sid = str(record_data["Sid"])
        set_date("sms_server", "sms_Sid", sid)
        mongo_status = record_data["Status"]
        mongo_phone = record_data["Phone"]
        mongo_Appid = record_data["Appid"]
        mongo_Tid = record_data["Tid"]
        mongo_Channel = record_data["Channel"]

        smsrecordcount_new = self.mongo_collection_count(SmsRecord,{'Appid': '100IME'}).count()
        print("短信发送后,该appid短信发送总条数：",smsrecordcount_new)

        condition_forAPP1 = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP1["StatisticsTime"] = yes_time
        condition_forAPPDay1 = condition_forAPP1
        AppofDay_count_new = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay1)
        print("短信发送后,APP每日短信量",AppofDay_count_new)
        condition_forAPP1["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth1 = condition_forAPP1
        AppofMonth_count_new = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth1)
        print("短信发送后,APP每月短信量",AppofMonth_count_new)

        condition_forChannel1 = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel1["StatisticsTime"] = yes_time
        condition_forChannelDay1 = condition_forChannel1
        ChannelOfDay_count_new =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay1)
        print("短信发送后,通道每日短信量",ChannelOfDay_count_new)
        condition_forChannel1["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth1 = condition_forChannel1
        ChannelOfMonth_count_new = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth1)
        print("短信发送后,通道每月短信量",ChannelOfMonth_count_new)

        condition_forTid1 = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid1["StatisticsTime"] = yes_time
        condition_forTidDay1 = condition_forTid1
        TidOfDay_count_new = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay1)
        print("短信发送后,短信模板每日短信量",TidOfDay_count_new)
        condition_forTid1["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth1 = condition_forTid1
        TidOfMonth_count_new = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth1)
        print("短信发送后,短信模板每月短信量",TidOfMonth_count_new)




        # 校验mongo 统计表数据存储
        difference = smsrecordcount_new-smsrecordcount_old
        self.assertEqual(AppofDay_count_old['TotalCount']+difference, AppofDay_count_new['TotalCount'])
        self.assertEqual(AppofMonth_count_old['TotalCount']+difference, AppofMonth_count_new['TotalCount'])
        self.assertEqual(ChannelOfDay_count_old['TotalCount']+difference, ChannelOfDay_count_new['TotalCount'])
        self.assertEqual(ChannelOfMonth_count_old['TotalCount']+difference, ChannelOfMonth_count_new['TotalCount'])
        self.assertEqual(TidOfDay_count_old['TotalCount']+difference, TidOfDay_count_new['TotalCount'])
        self.assertEqual(TidOfMonth_count_old['TotalCount']+difference, TidOfMonth_count_new['TotalCount'])
        # 校验ES
        resp_doc_new = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_new = resp_doc_new['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_new)

        query_ES = {"query": {"match": {"_id": ""}}}
        query_ES["query"]["match"]["_id"] = sid
        set_date("ES", "query_content", query_ES)
        ES_query_content = get_data("ES","query_content").replace('\'','"')
        print(ES_query_content)
        resp_doc_new2 = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_content)
        print(resp_doc_new2)
        ES_appid = resp_doc_new2["hits"]["hits"][0]["_source"]["appid"]
        ES_phone = resp_doc_new2["hits"]["hits"][0]["_source"]["phone"]
        ES_channel = resp_doc_new2["hits"]["hits"][0]["_source"]["channel"]
        ES_tid = resp_doc_new2["hits"]["hits"][0]["_source"]["tid"]
        ES_status = resp_doc_new2["hits"]["hits"][0]["_source"]["status"]
        print("ES_appid:",ES_appid,"ES_phone:",ES_phone,"ES_channel:",ES_channel,"ES_tid:",ES_tid,"ES_status:",ES_status)
        self.assertEqual(mongo_Appid,ES_appid)
        self.assertEqual(mongo_Channel,ES_channel)
        self.assertEqual(mongo_phone,ES_phone)
        self.assertEqual(mongo_Tid,ES_tid)
        self.assertEqual(mongo_status,ES_status)

    def test_02(self):
        ''' 验证consumer 计费 和 统计 '''
        SmsRecord = get_data("mongo_integration","collection1")
        SmsStatisticsForAppOfDay = get_data("mongo_integration","collection2")
        SmsStatisticsForAppOfMonth = get_data("mongo_integration","collection3")
        SmsStatisticsForChannelOfDay = get_data("mongo_integration","collection4")
        SmsStatisticsForChannelOfMonth = get_data("mongo_integration","collection5")
        SmsStatisticsForTidOfDay = get_data("mongo_integration","collection6")
        SmsStatisticsForTidOfMonth = get_data("mongo_integration","collection7")

        ES_host = get_data("ES", "servers")
        ES_index = get_data("ES", "index")
        ES_query_total = get_data("ES", "query_total")

        yes_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print yes_time

        condition_forAPP = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP["StatisticsTime"] = yes_time[:10]
        condition_forAPPDay = condition_forAPP
        AppofDay_count_old = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay)
        print("APP每日短信量",AppofDay_count_old)
        condition_forAPP["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth = condition_forAPP
        AppofMonth_count_old = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth)
        print("APP每月短信量",AppofMonth_count_old)

        condition_forChannel = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel["StatisticsTime"] = yes_time[:10]
        condition_forChannelDay = condition_forChannel
        ChannelOfDay_count_old =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay)
        print("通道每日短信量",ChannelOfDay_count_old)
        condition_forChannel["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth = condition_forChannel
        ChannelOfMonth_count_old = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth)
        print("通道每月短信量",ChannelOfMonth_count_old)

        condition_forTid = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid["StatisticsTime"] = yes_time[:10]
        condition_forTidDay = condition_forTid
        TidOfDay_count_old = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay)
        print("短信模板每日短信量",TidOfDay_count_old)
        condition_forTid["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth = condition_forTid
        TidOfMonth_count_old = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth)
        print("短信模板每月短信量",TidOfMonth_count_old)


        resp_doc = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_old = resp_doc['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_old)

        #
        # # # #
        Sid = get_data("sms_server","sms_sid")
        # post 请求体 内容，并将验证码添加至请求体重
        body_content = [{"user_receive_time": "","nationcode": "86","mobile": "18856361920","report_status": "SUCCESS","errmsg": "DELIVRD","description": "用户短信送达成功","sid": ""}]
        body_content[0]["user_receive_time"] = str(yes_time)
        body_content[0]["sid"] = str(Sid)
        # 向接口发送请求
        r = requests.post(url=self.urlcallbacktencent, json=body_content)
        print("接口返回信息：",r.text)
        # 校验接口返回信息
        self.assertEqual(r.text,'{"errmsg":"OK","result":0}')
        time.sleep(15)

        '''#### 验证消息插件功能 #####'''
        query_criteria = {"Sid" : ""}
        query_criteria["Sid"] = Sid
        record_data = self.mongo_Recordquery(query_criteria)
        print("mongo历史记录表查询数据：", record_data)
        sid = str(record_data["Sid"])
        set_date("sms_server", "sms_Sid", sid)
        mongo_status = record_data["Status"]


        condition_forAPP1 = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP1["StatisticsTime"] = yes_time[:10]
        condition_forAPPDay1 = condition_forAPP1
        AppofDay_count_new = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay1)
        print("短信发送后,APP每日短信量",AppofDay_count_new)
        condition_forAPP1["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth1 = condition_forAPP1
        AppofMonth_count_new = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth1)
        print("短信发送后,APP每月短信量",AppofMonth_count_new)

        condition_forChannel1 = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel1["StatisticsTime"] = yes_time[:10]
        condition_forChannelDay1 = condition_forChannel1
        ChannelOfDay_count_new =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay1)
        print("短信发送后,通道每日短信量",ChannelOfDay_count_new)
        condition_forChannel1["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth1 = condition_forChannel1
        ChannelOfMonth_count_new = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth1)
        print("短信发送后,通道每月短信量",ChannelOfMonth_count_new)

        condition_forTid1 = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid1["StatisticsTime"] = yes_time[:10]
        condition_forTidDay1 = condition_forTid1
        TidOfDay_count_new = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay1)
        print("短信发送后,短信模板每日短信量",TidOfDay_count_new)
        condition_forTid1["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth1 = condition_forTid1
        TidOfMonth_count_new = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth1)
        print("短信发送后,短信模板每月短信量",TidOfMonth_count_new)




        # 校验mongo 统计表数据存储
        # self.assertEqual(AppofDay_count_old['TotalCount']+1, AppofDay_count_new['TotalCount'])
        # self.assertEqual(AppofMonth_count_old['TotalCount']+1, AppofMonth_count_new['TotalCount'])
        # self.assertEqual(ChannelOfDay_count_old['TotalCount']+1, ChannelOfDay_count_new['TotalCount'])
        # self.assertEqual(ChannelOfMonth_count_old['TotalCount']+1, ChannelOfMonth_count_new['TotalCount'])
        # self.assertEqual(TidOfDay_count_old['TotalCount']+1, TidOfDay_count_new['TotalCount'])
        # self.assertEqual(TidOfMonth_count_old['TotalCount']+1, TidOfMonth_count_new['TotalCount'])

        self.assertEqual(AppofDay_count_old['SuccessCount']+1, AppofDay_count_new['SuccessCount'])
        self.assertEqual(AppofMonth_count_old['SuccessCount']+1, AppofMonth_count_new['SuccessCount'])
        self.assertEqual(ChannelOfDay_count_old['SuccessCount']+1, ChannelOfDay_count_new['SuccessCount'])
        self.assertEqual(ChannelOfMonth_count_old['SuccessCount']+1, ChannelOfMonth_count_new['SuccessCount'])
        self.assertEqual(TidOfDay_count_old['SuccessCount']+1, TidOfDay_count_new['SuccessCount'])
        self.assertEqual(TidOfMonth_count_old['SuccessCount']+1, TidOfMonth_count_new['SuccessCount'])

        self.assertEqual(AppofDay_count_old['ChargedCount']+1, AppofDay_count_new['ChargedCount'])
        self.assertEqual(AppofMonth_count_old['ChargedCount']+1, AppofMonth_count_new['ChargedCount'])
        self.assertEqual(ChannelOfDay_count_old['ChargedCount']+1, ChannelOfDay_count_new['ChargedCount'])
        self.assertEqual(ChannelOfMonth_count_old['ChargedCount']+1, ChannelOfMonth_count_new['ChargedCount'])
        self.assertEqual(TidOfDay_count_old['ChargedCount']+1, TidOfDay_count_new['ChargedCount'])
        self.assertEqual(TidOfMonth_count_old['ChargedCount']+1, TidOfMonth_count_new['ChargedCount'])
        # 校验ES
        resp_doc_new = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_new = resp_doc_new['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_new)

        query_ES = {"query": {"match": {"_id": ""}}}
        query_ES["query"]["match"]["_id"] = Sid
        set_date("ES", "query_content", query_ES)
        ES_query_content = get_data("ES","query_content").replace('\'','"')
        print(ES_query_content)
        resp_doc_new2 = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_content)
        print(resp_doc_new2)
        ES_status = resp_doc_new2["hits"]["hits"][0]["_source"]["status"]
        ES_status = resp_doc_new2["hits"]["hits"][0]["_source"]["status"]
        print("ES_status:",ES_status)
        self.assertEqual(mongo_status,ES_status)

    def test_03(self):
        ''' 验证consumer 发送单条短信 字符为70字 '''
        SmsRecord = get_data("mongo_integration","collection1")
        SmsStatisticsForAppOfDay = get_data("mongo_integration","collection2")
        SmsStatisticsForAppOfMonth = get_data("mongo_integration","collection3")
        SmsStatisticsForChannelOfDay = get_data("mongo_integration","collection4")
        SmsStatisticsForChannelOfMonth = get_data("mongo_integration","collection5")
        SmsStatisticsForTidOfDay = get_data("mongo_integration","collection6")
        SmsStatisticsForTidOfMonth = get_data("mongo_integration","collection7")

        ES_host = get_data("ES", "servers")
        ES_index = get_data("ES", "index")
        ES_query_total = get_data("ES", "query_total")

        yes_time = datetime.datetime.now().strftime('%Y-%m-%d')
        # print yes_time

        smsrecordcount_old = self.mongo_collection_count(SmsRecord,{'Appid': '100IME'}).count()
        print("该appid短信发送总条数：",smsrecordcount_old)

        condition_forAPP = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP["StatisticsTime"] = yes_time
        condition_forAPPDay = condition_forAPP
        AppofDay_count_old = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay)
        print("APP每日短信量",AppofDay_count_old)
        condition_forAPP["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth = condition_forAPP
        AppofMonth_count_old = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth)
        print("APP每月短信量",AppofMonth_count_old)

        condition_forChannel = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel["StatisticsTime"] = yes_time
        condition_forChannelDay = condition_forChannel
        ChannelOfDay_count_old =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay)
        print("通道每日短信量",ChannelOfDay_count_old)
        condition_forChannel["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth = condition_forChannel
        ChannelOfMonth_count_old = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth)
        print("通道每月短信量",ChannelOfMonth_count_old)

        condition_forTid = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid["StatisticsTime"] = yes_time
        condition_forTidDay = condition_forTid
        TidOfDay_count_old = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay)
        print("短信模板每日短信量",TidOfDay_count_old)
        condition_forTid["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth = condition_forTid
        TidOfMonth_count_old = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth)
        print("短信模板每月短信量",TidOfMonth_count_old)


        resp_doc = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_old = resp_doc['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_old)

        #
        # # # #
        code_num = int(time.time())  # 构建一个验证码；按时间构建保证唯一性 并和目前使用验证码不冲突
        print("code_num：",code_num)
        # post 请求体 内容，并将验证码添加至请求体重
        body_content = {"appid": "100IME","phone": ["18856361920"],"tid": "10205","tp": "{'Code':'', 'Seq':'999', 'Minute':'50'}"}
        code_content= {'Code':'', 'Seq':'999', 'Minute':'50'}
        code_content['Code'] = str(code_num) + "1"*19
        body_content["tp"] = code_content
        # 向接口发送请求
        r = requests.post(url=self.url,json=body_content)
        print("接口返回信息：", r.text)
        # 校验接口返回信息
        self.assertEqual(r.text, '{"code":"000000","desc":"成功"}')
        time.sleep(15)
        '''#### 验证消息插件功能 #####'''
        # 构建查询条件
        query_criteria = {"Content":""}
        query_criteria["Content"] = "【科大讯飞】您好，您本次操作的验证码为%s，序号为999。请在50分钟内使用，过期无效。" % (str(code_num) + "1"*19)
        record_data = self.mongo_Recordquery(query_criteria)
        print("mongo历史记录表查询数据：", record_data)
        sid = str(record_data["Sid"])
        set_date("sms_server", "sms_Sid", sid)
        mongo_status = record_data["Status"]
        mongo_phone = record_data["Phone"]
        mongo_Appid = record_data["Appid"]
        mongo_Tid = record_data["Tid"]
        mongo_Channel = record_data["Channel"]

        smsrecordcount_new = self.mongo_collection_count(SmsRecord,{'Appid': '100IME'}).count()
        print("短信发送后,该appid短信发送总条数：",smsrecordcount_new)

        condition_forAPP1 = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP1["StatisticsTime"] = yes_time
        condition_forAPPDay1 = condition_forAPP1
        AppofDay_count_new = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay1)
        print("短信发送后,APP每日短信量",AppofDay_count_new)
        condition_forAPP1["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth1 = condition_forAPP1
        AppofMonth_count_new = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth1)
        print("短信发送后,APP每月短信量",AppofMonth_count_new)

        condition_forChannel1 = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel1["StatisticsTime"] = yes_time
        condition_forChannelDay1 = condition_forChannel1
        ChannelOfDay_count_new =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay1)
        print("短信发送后,通道每日短信量",ChannelOfDay_count_new)
        condition_forChannel1["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth1 = condition_forChannel1
        ChannelOfMonth_count_new = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth1)
        print("短信发送后,通道每月短信量",ChannelOfMonth_count_new)

        condition_forTid1 = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid1["StatisticsTime"] = yes_time
        condition_forTidDay1 = condition_forTid1
        TidOfDay_count_new = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay1)
        print("短信发送后,短信模板每日短信量",TidOfDay_count_new)
        condition_forTid1["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth1 = condition_forTid1
        TidOfMonth_count_new = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth1)
        print("短信发送后,短信模板每月短信量",TidOfMonth_count_new)




        # 校验mongo 统计表数据存储
        difference = smsrecordcount_new-smsrecordcount_old
        self.assertEqual(AppofDay_count_old['TotalCount']+difference, AppofDay_count_new['TotalCount'])
        self.assertEqual(AppofMonth_count_old['TotalCount']+difference, AppofMonth_count_new['TotalCount'])
        self.assertEqual(ChannelOfDay_count_old['TotalCount']+difference, ChannelOfDay_count_new['TotalCount'])
        self.assertEqual(ChannelOfMonth_count_old['TotalCount']+difference, ChannelOfMonth_count_new['TotalCount'])
        self.assertEqual(TidOfDay_count_old['TotalCount']+difference, TidOfDay_count_new['TotalCount'])
        self.assertEqual(TidOfMonth_count_old['TotalCount']+difference, TidOfMonth_count_new['TotalCount'])
        # 校验ES
        resp_doc_new = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_new = resp_doc_new['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_new)

        query_ES = {"query": {"match": {"_id": ""}}}
        query_ES["query"]["match"]["_id"] = sid
        set_date("ES", "query_content", query_ES)
        ES_query_content = get_data("ES","query_content").replace('\'','"')
        print(ES_query_content)
        resp_doc_new2 = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_content)
        print(resp_doc_new2)
        ES_appid = resp_doc_new2["hits"]["hits"][0]["_source"]["appid"]
        ES_phone = resp_doc_new2["hits"]["hits"][0]["_source"]["phone"]
        ES_channel = resp_doc_new2["hits"]["hits"][0]["_source"]["channel"]
        ES_tid = resp_doc_new2["hits"]["hits"][0]["_source"]["tid"]
        ES_status = resp_doc_new2["hits"]["hits"][0]["_source"]["status"]
        print("ES_appid:",ES_appid,"ES_phone:",ES_phone,"ES_channel:",ES_channel,"ES_tid:",ES_tid,"ES_status:",ES_status)
        self.assertEqual(mongo_Appid,ES_appid)
        self.assertEqual(mongo_Channel,ES_channel)
        self.assertEqual(mongo_phone,ES_phone)
        self.assertEqual(mongo_Tid,ES_tid)
        self.assertEqual(mongo_status,ES_status)

    def test_04(self):
        ''' 验证consumer 计费单条短信字数>=70，计两条 '''
        SmsRecord = get_data("mongo_integration","collection1")
        SmsStatisticsForAppOfDay = get_data("mongo_integration","collection2")
        SmsStatisticsForAppOfMonth = get_data("mongo_integration","collection3")
        SmsStatisticsForChannelOfDay = get_data("mongo_integration","collection4")
        SmsStatisticsForChannelOfMonth = get_data("mongo_integration","collection5")
        SmsStatisticsForTidOfDay = get_data("mongo_integration","collection6")
        SmsStatisticsForTidOfMonth = get_data("mongo_integration","collection7")

        ES_host = get_data("ES", "servers")
        ES_index = get_data("ES", "index")
        ES_query_total = get_data("ES", "query_total")

        yes_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # print yes_time

        condition_forAPP = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP["StatisticsTime"] = yes_time[:10]
        condition_forAPPDay = condition_forAPP
        AppofDay_count_old = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay)
        print("APP每日短信量",AppofDay_count_old)
        condition_forAPP["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth = condition_forAPP
        AppofMonth_count_old = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth)
        print("APP每月短信量",AppofMonth_count_old)

        condition_forChannel = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel["StatisticsTime"] = yes_time[:10]
        condition_forChannelDay = condition_forChannel
        ChannelOfDay_count_old =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay)
        print("通道每日短信量",ChannelOfDay_count_old)
        condition_forChannel["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth = condition_forChannel
        ChannelOfMonth_count_old = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth)
        print("通道每月短信量",ChannelOfMonth_count_old)

        condition_forTid = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid["StatisticsTime"] = yes_time[:10]
        condition_forTidDay = condition_forTid
        TidOfDay_count_old = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay)
        print("短信模板每日短信量",TidOfDay_count_old)
        condition_forTid["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth = condition_forTid
        TidOfMonth_count_old = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth)
        print("短信模板每月短信量",TidOfMonth_count_old)


        resp_doc = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_old = resp_doc['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_old)

        #
        # # # #
        Sid = get_data("sms_server","sms_sid")
        # post 请求体 内容，并将验证码添加至请求体重
        body_content = [{"user_receive_time": "","nationcode": "86","mobile": "18856361920","report_status": "SUCCESS","errmsg": "DELIVRD","description": "用户短信送达成功","sid": ""}]
        body_content[0]["user_receive_time"] = str(yes_time)
        body_content[0]["sid"] = str(Sid)
        # 向接口发送请求
        r = requests.post(url=self.urlcallbacktencent, json=body_content)
        print("接口返回信息：",r.text)
        # 校验接口返回信息
        self.assertEqual(r.text,'{"errmsg":"OK","result":0}')
        time.sleep(15)

        '''#### 验证消息插件功能 #####'''
        query_criteria = {"Sid" : ""}
        query_criteria["Sid"] = Sid
        record_data = self.mongo_Recordquery(query_criteria)
        print("mongo历史记录表查询数据：", record_data)
        sid = str(record_data["Sid"])
        set_date("sms_server", "sms_Sid", sid)
        mongo_status = record_data["Status"]


        condition_forAPP1 = {"Appid":"100IME","StatisticsTime":""}
        condition_forAPP1["StatisticsTime"] = yes_time[:10]
        condition_forAPPDay1 = condition_forAPP1
        AppofDay_count_new = self.sms_count(SmsStatisticsForAppOfDay,condition_forAPPDay1)
        print("短信发送后,APP每日短信量",AppofDay_count_new)
        condition_forAPP1["StatisticsTime"] = yes_time[:7]
        condition_forAPPmonth1 = condition_forAPP1
        AppofMonth_count_new = self.sms_count(SmsStatisticsForAppOfMonth,condition_forAPPmonth1)
        print("短信发送后,APP每月短信量",AppofMonth_count_new)

        condition_forChannel1 = {"Appid": "100IME", "StatisticsTime": "", "Channel": "tencent"}
        condition_forChannel1["StatisticsTime"] = yes_time[:10]
        condition_forChannelDay1 = condition_forChannel1
        ChannelOfDay_count_new =self.sms_count(SmsStatisticsForChannelOfDay,condition_forChannelDay1)
        print("短信发送后,通道每日短信量",ChannelOfDay_count_new)
        condition_forChannel1["StatisticsTime"] = yes_time[:7]
        condition_forChannelMonth1 = condition_forChannel1
        ChannelOfMonth_count_new = self.sms_count(SmsStatisticsForChannelOfMonth,condition_forChannelMonth1)
        print("短信发送后,通道每月短信量",ChannelOfMonth_count_new)

        condition_forTid1 = {"Appid": "100IME", "StatisticsTime": "", "Tid": "10205"}
        condition_forTid1["StatisticsTime"] = yes_time[:10]
        condition_forTidDay1 = condition_forTid1
        TidOfDay_count_new = self.sms_count(SmsStatisticsForTidOfDay,condition_forTidDay1)
        print("短信发送后,短信模板每日短信量",TidOfDay_count_new)
        condition_forTid1["StatisticsTime"] = yes_time[:7]
        condition_forTidMonth1 = condition_forTid1
        TidOfMonth_count_new = self.sms_count(SmsStatisticsForTidOfMonth,condition_forTidMonth1)
        print("短信发送后,短信模板每月短信量",TidOfMonth_count_new)




        # 校验mongo 统计表数据存储
        # self.assertEqual(AppofDay_count_old['TotalCount']+1, AppofDay_count_new['TotalCount'])
        # self.assertEqual(AppofMonth_count_old['TotalCount']+1, AppofMonth_count_new['TotalCount'])
        # self.assertEqual(ChannelOfDay_count_old['TotalCount']+1, ChannelOfDay_count_new['TotalCount'])
        # self.assertEqual(ChannelOfMonth_count_old['TotalCount']+1, ChannelOfMonth_count_new['TotalCount'])
        # self.assertEqual(TidOfDay_count_old['TotalCount']+1, TidOfDay_count_new['TotalCount'])
        # self.assertEqual(TidOfMonth_count_old['TotalCount']+1, TidOfMonth_count_new['TotalCount'])

        self.assertEqual(AppofDay_count_old['SuccessCount']+1, AppofDay_count_new['SuccessCount'])
        self.assertEqual(AppofMonth_count_old['SuccessCount']+1, AppofMonth_count_new['SuccessCount'])
        self.assertEqual(ChannelOfDay_count_old['SuccessCount']+1, ChannelOfDay_count_new['SuccessCount'])
        self.assertEqual(ChannelOfMonth_count_old['SuccessCount']+1, ChannelOfMonth_count_new['SuccessCount'])
        self.assertEqual(TidOfDay_count_old['SuccessCount']+1, TidOfDay_count_new['SuccessCount'])
        self.assertEqual(TidOfMonth_count_old['SuccessCount']+1, TidOfMonth_count_new['SuccessCount'])

        self.assertEqual(AppofDay_count_old['ChargedCount']+2, AppofDay_count_new['ChargedCount'])
        self.assertEqual(AppofMonth_count_old['ChargedCount']+2, AppofMonth_count_new['ChargedCount'])
        self.assertEqual(ChannelOfDay_count_old['ChargedCount']+2, ChannelOfDay_count_new['ChargedCount'])
        self.assertEqual(ChannelOfMonth_count_old['ChargedCount']+2, ChannelOfMonth_count_new['ChargedCount'])
        self.assertEqual(TidOfDay_count_old['ChargedCount']+2, TidOfDay_count_new['ChargedCount'])
        self.assertEqual(TidOfMonth_count_old['ChargedCount']+2, TidOfMonth_count_new['ChargedCount'])
        # 校验ES
        resp_doc_new = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_total)
        ES_total_new = resp_doc_new['hits']["total"]
        print("ES 该APP下日志记录总数为：",ES_total_new)

        query_ES = {"query": {"match": {"_id": ""}}}
        query_ES["query"]["match"]["_id"] = Sid
        set_date("ES", "query_content", query_ES)
        ES_query_content = get_data("ES","query_content").replace('\'','"')
        print(ES_query_content)
        resp_doc_new2 = Elasticsearch_Init().operation_ES(ES_host,ES_index,ES_query_content)
        print(resp_doc_new2)
        ES_status = resp_doc_new2["hits"]["hits"][0]["_source"]["status"]
        ES_status = resp_doc_new2["hits"]["hits"][0]["_source"]["status"]
        print("ES_status:",ES_status)
        self.assertEqual(mongo_status,ES_status)

    def mongo_Recordquery(self,condition):
        #获取mongo信息 链接mongo
        host = get_data("mongo_integration","mongohost")
        port = int(get_data("mongo_integration","port"))
        database = get_data("mongo_integration","database")
        SmsRecord = get_data("mongo_integration","collection1")
        data = Mongo().connect_mongo(host=host,port=port,database=database,collection=SmsRecord).find_one(condition)
        return data
    def mongo_collection_count(self,collection,condition):
        host = get_data("mongo_integration","mongohost")
        port = int(get_data("mongo_integration","port"))
        database = get_data("mongo_integration","database")
        data = Mongo().connect_mongo(host=host,port=port,database=database,collection=collection).find(condition)
        return data
    def sms_count(self,collection,condition):
        data = self.mongo_collection_count(collection, condition)
        Sms_count = [i for i in data]
        if len(Sms_count) == 0:
            TotalCount = 0
            ChargedCount = 0
            SuccessCount = 0
        else:
            TotalCount = Sms_count[0]['TotalCount']
            ChargedCount = Sms_count[0]['ChargedCount']
            SuccessCount = Sms_count[0]['SuccessCount']
        SMS_count = {"TotalCount":TotalCount,"ChargedCount":ChargedCount,"SuccessCount":SuccessCount}
        return SMS_count



if __name__ == '__main__':
    unittest.main()