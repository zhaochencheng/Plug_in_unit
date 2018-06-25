#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 15:55
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Mongo_Client.py
# @Software: PyCharm
import logging as log
log.basicConfig(level=log.DEBUG)
from pymongo import MongoClient
from Plug_in_unit.public_script.function_public import *
import datetime
import sys
import json
class Mongo():
    '''
    #函数作用：mongo 连接初始化并返回链接实例
    #参数说明：host:       mongo 链接地址
    #         port:         mongo 链接端口
    #         database:     mongo 链接数据库
    #         collection:   mongo 连接集合（表）
    #
    #兼容 Python2 和 python3
    #
    '''
    #初始化化数据
    host = get_data("mongo","mongohost")
    port = int(get_data("mongo","port"))
    database = get_data("mongo","database")
    collection = get_data("mongo","collection")
    def __init__(self):
        pass
    def connect_mongo(self):
        if sys.version_info.major == 2:
            client = MongoClient(self.host,port=self.port)
            #获取数据库
            db = client[self.database]
            # print("当前连接数据库为：", db)
            #获取集合
            collections = db[self.collection]
            # print("当前获取集合（表）:", collections)
            return collections
        elif sys.version_info.major == 3:
            client = MongoClient(self.host,port=self.port)
            #获取数据库
            db = client[self.database]
            # print("当前连接数据库为：", db)
            #获取集合
            collections = db[self.collection]
            # print("当前获取集合（表）:", collections)
            return collections

if __name__ == '__main__':
    data = get_data("mongo","data")
    # data = '{"author":"mike","text":"123","tags":["mongodb","python"],"date":123}'
    print(data, type(data))
    data2 = json.loads(data)
    print(data2, type(data2))

    mongo = Mongo()
    mongo.connect_mongo().insert_one(json.loads(data))