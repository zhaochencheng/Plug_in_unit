#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 13:48
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : redis_init.py
# @Software: PyCharm
import redis
import logging as log
log.basicConfig(level=log.DEBUG)
from Plug_in_unit.public_script.function_public import *
import sys
class redis_init():
    '''
    #函数作用：Redis连接初始化，返回redis连接对象；
    #参数说明：host：      redis 连接地址
    #         port：      redis 链接端口。默认=6379
    #         database：  redis 查询的数据库

    #兼容 Python2 和 python3
    #python2  r.get("key")----返回数据类型为type()==str;
    #python3  r.get("key")----返回数据类型type() == bytes
            bytes <<-->> str:
                str to bytes :bytes(s,encoding = "utf-8") or  str.encode(s)
                bytes to str :str(s,encoding = "utf-8") or  bytes.decode(s)
    '''
    #初始化数据
    host = get_data("redis", "server_host")
    port = get_data("redis", "server_port")
    database = get_data("redis","server_database")

    def redis_opearte(self):
        if sys.version_info.major == 2:
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.database)
            r =redis.Redis(connection_pool=pool)
            return r
        elif sys.version_info.major == 3:
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.database)
            r =redis.Redis(connection_pool=pool)
            return r
if __name__ == '__main__':
    red = redis_init()
    a = red.redis_opearte().get("TSN_SERIAL_NUMBER_20180508140401")
    print(a,type(a))
    # print(sys.getdefaultencoding())
    # b =str(a,encoding='utf-8')
    # print(b,type(b))
    b = bytes.decode(a)
    print(b, type(b))