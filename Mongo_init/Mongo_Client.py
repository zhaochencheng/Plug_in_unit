#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 15:55
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Mongo_Client.py
# @Software: PyCharm
import pymongo
from pymongo import MongoClient
import pprint
import datetime

# client = MongoClient()
# client = MongoClient("192.168.45.104", port=27017)
# #获取数据库
# db = client['DripAudit']
# #获取集合collection(表)
# collection = db['test']
# print collection.find_one({"Appid":"100IME"})
# pprint.pprint(collection.find_one({"Appid":"100IME"}))
# post = {"author":"mike","text":"我的第一盘","tags":["mongodb","python"],"date":datetime.datetime.utcnow()}
# collection.insert(post)
# print collection.insert_one(post).inserted_id
#插入数据用 insert_one or insert_many ;insert 不建议使用
# post_id = collection.insert_one(post).inserted_id

# print collection.find_one({"author":"mike"})
# print collection.count()
# print collection.name
#查询find or find_one
# pprint.pprint(collection.find_one({"_id":post_id}))
# for post in collection.find({"author":"mike"}):
#     pprint.pprint(post)
#     print '\n'
# all = collection.find({})
# print all
import json
from Plug_in_unit.public_script.function_public import *

# class Mongo():
#     def __init__(self):
#         self.host = get_data("mongo","mongohost")
#         self.port = int(get_data("mongo","port"))
#         self.database = get_data("mongo","database")
#         self.collection = get_data("mongo","collection")
#         self.data = get_data("mongo","data")
#
#     def connect_mongo(self):
#         client = MongoClient(self.host,port=self.port)
#         #获取数据库
#         db = client[self.database]
#         print "当前连接数据库为：",db
#         #获取集合
#         collections = db[self.collection]
#         print "当前获取集合（表）:",collections
#         return collections
#     def mongo_insert(self):
#         client = pymongo.MongoClient(self.host,self.port)
#         db = client[self.database]
#         collections = db[self.collection]
#         print collections.count()
#         collections.insert_one()
#         print collections.count()
#         # print self.connect_mongo().count()
#         # self.connect_mongo().insert_one(self.data)
#         # print self.connect_mongo().count()

if __name__ == '__main__':
    data = get_data("mongo","data")
    print data,type(data)
    print
    # print json.loads(text),type(json.loads(text).decode("utf-8").encode("gb2312"))
    # mongo = Mongo()
    # # mongo.connect_mongo()
    # mongo.mongo_insert()


#
