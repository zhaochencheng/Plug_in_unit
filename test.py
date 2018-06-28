#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/22 11:53
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : test.py
# @Software: PyCharm
# import sys
# print(sys.version_info)
# if sys.version_info.major == 3 :
#     print(666)
import random
import time,datetime
# print(time.time())
# time.sleep(1)
# print(time.time())
# time.sleep(1)
# print(time.time())
#
# print time.mktime(datetime.datetime.now().timetuple())
# print time.mktime(datetime.datetime.now().timetuple())
# print time.mktime(datetime.datetime.now().timetuple())
# time.sleep(0.1)
# print time.mktime(datetime.datetime.now().timetuple())
# print time.mktime(datetime.datetime.now().timetuple())
# stm = '2018-06-27 18:19:15'
# print stm[0:10]
#格式化输出
# yes_time = datetime.datetime.now().strftime('%Y-%m-%d')
# print yes_time
# # code = random.randrange(1,100)
# print code
# code1 = 2018003318+code
# print code1
# code = time.time()
# code_content = {'msgcontent':''}
# code_content['msgcontent'] = code
# body = {"appid": "OD0QS8Z6","phone": ["18856361920"],"tid": "10202","tp": "{'msgcontent':''}"}
#
# code_content = body["tp"]
# r = {"code":"000000","desc":"成功"}
# print r["code"],type(r["code"])
# r = {"Content" : "【科大讯飞】1530087810"}
# b = {"Content":""}
# content = "【科大讯飞】"+"1530087810"
# print content
# b["Content"] = content
# print b
# from Plug_in_unit.public_script.function_public import *
# query_ES = {"query": {"match": {"_id": "2cb6d8b349c44aabab53b0facef0ca49:7081684480555158"}}}
# print query_ES["query"]["match"]["_id"]
# query_ES["query"]["match"]["_id"] = '2245153'
# print query_ES
# set_date("ES","query_content",query_ES)
# myStr = str({"query": {"match": {"_id": "2cb6d8b349c44aabab53b0facef0ca49:7081684480555158"}}})
# myStr = myStr.replace('"','\'')
# print myStr
import requests
# body_content = {"appid": "OD0QS8Z6","phone": ["18856361920"],"tid": "10202","tp": "{'msgcontent':''}"}
# code_content= {'msgcontent':''}
# code_content['msgcontent'] = "1452"
# body_content["tp"] = code_content
# #向接口发送请求
# r = requests.post(url='http://172.16.82.142:8081/sms',json=body_content)
# print("接口返回信息：",r.content)
# print(r.text)
# query_ES = {"query": {"match": {"_id": ""}}}
# print(type(query_ES))
# query_ES["query"]["match"]["_id"] = "213"
# print(query_ES,type(query_ES))
# code_num =1232312312
# p = "【科大讯飞】您好，您本次操作的验证码为%s，序号为2018/5/222。请在50分钟内使用，过期无效。" % str(code_num)
# print(p)
# body_content = [{"user_receive_time": "2018-06-28 15:26:22","nationcode": "86","mobile": "18856361920","report_status": "SUCCESS","errmsg": "DELIVRD","description": "用户短信送达成功","sid": ""}]
# code_content= body_content[0]["sid"]
# print(code_content)
# yes_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
# print(yes_time)
# body_content[0]["user_receive_time"] = str(yes_time)
# print(body_content)
body_content = [{"user_receive_time": "","nationcode": "86","mobile": "18856361920","report_status": "SUCCESS","errmsg": "DELIVRD","description": "用户短信送达成功","sid": ""}]
# body_content[0]["user_receive_time"] = str(yes_time)
# body_content[0]["sid"] = str(Sid)
# 向接口发送请求
# r = requests.post(url='http://172.16.82.142:8081/sms/tencent/record', json=body_content)
# print("接口返回信息：",r.text)
# 校验接口返回信息
# self.assertEqual(r.text,'{"errmsg":"OK","result":0}')
code = "1455"+'1'*34
body_content = {"appid": "100IME","phone": ["18856361920"],"tid": "10205","tp": "{'Code':'', 'Seq':'999', 'Minute':'50'}"}
code_content= {'Code':'', 'Seq':'999', 'Minute':'50'}
code_content['Code'] = "1455"+'1'*34
print(code_content)