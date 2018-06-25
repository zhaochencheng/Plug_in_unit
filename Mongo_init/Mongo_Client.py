#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 15:55
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Mongo_Client.py
# @Software: PyCharm
import pymongo
from pymongo import MongoClient
from Plug_in_unit.public_script.function_public import *

class Mongo():
     #初始化化数据
    host = get_data("mongo","mongohost")
    port = int(get_data("mongo","port"))
    database = get_data("mongo","database")
    collection = get_data("mongo","collection")
    data = get_data("mongo","data")
    def __init__(self):
        pass
    def connect_mongo(self):
        client = MongoClient(self.host,port=self.port)
        #获取数据库
        db = client[self.database]
        print("当前连接数据库为：",db)
        #获取集合
        collections = db[self.collection]
        print("当前获取集合（表）:",collections)
        return collections
    def mongo_insert(self):
        client = pymongo.MongoClient(self.host,self.port)
        db = client[self.database]
        collections = db[self.collection]
        print(collections.count())
        collections.insert_one(self.data)
        print(collections.count())
        # print self.connect_mongo().count()
        # self.connect_mongo().insert_one(self.data)
        # print self.connect_mongo().count()

if __name__ == '__main__':
    data = get_data("mongo","data")
    print(data,type(data))
    print(data.split(","))
    # print(data1,type(data1))



    # mongo = Mongo()
    # # mongo.connect_mongo()
    # mongo.mongo_insert()


#
