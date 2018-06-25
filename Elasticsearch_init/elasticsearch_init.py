#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/25 9:21
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : elasticsearch_init.py
# @Software: PyCharm

from elasticsearch import Elasticsearch
import logging as log
log.basicConfig(level=log.DEBUG)

from Plug_in_unit.public_script.function_public import *
import json
import sys
class Elasticsearch_Init():
    '''
    #函数作用：从参数文件中写入参数值
    #参数说明：index ES中的索引（相当于数据库中的database）
    #         query 查询条件/查询语句
    #         resp  ES查询结果，返回type = dict（字典）
    #兼容 Python2 和 python3
    '''
    #初始化数据
    host = get_data("ES", "servers")
    index = get_data("ES", "index")
    query = get_data("ES", "query")

    def operation_ES(self):
        if sys.version_info.major == 2:
            es = Elasticsearch([self.host])
            index = self.index
            query = self.query
            #json.loads   str 转化为 dict
            resp = es.search(index=index, body=json.loads(query))
            return resp
        elif sys.version_info.major == 3:
            es = Elasticsearch([self.host])
            index = self.index
            query = self.query
            resp = es.search(index=index, body=json.loads(query))
            return resp

if __name__ == '__main__':
    Es = Elasticsearch_Init()
    resp_doc = Es.operation_ES()
    print resp_doc['hits']['hits'][0]["_source"]["extra"]
    print type(resp_doc)
    resp1 = json.dumps(resp_doc,ensure_ascii=False)
    print resp1
    print type(resp1)
