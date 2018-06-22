#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 14:26
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Producer_init.py
# @Software: PyCharm
from pykafka import KafkaClient
import sys
from Plug_in_unit.public_script.function_public import *
import logging as log
log.basicConfig(level=log.DEBUG)

class Kafka_Producer():

    #初始化数据
    hostname= get_data("kafka2","hostname")
    topic = get_data("kafka2","topics")
    msg = get_data("kafka2","producer_msg")

    def producer_init(self):
        '''
        生产者 向kafka中 push 消息
        '''
        if sys.version_info.major == 2:
            log.basicConfig(level=log.DEBUG)
            client = KafkaClient(hosts=self.hostname)
            print(client.topics)
            Topic = client.topics[self.topic]
            producer = Topic.get_producer()
            producer.produce(self.msg)
            print(self.msg)
            producer.stop()
        elif sys.version_info.major == 3:
            pass

if __name__ == '__main__':
    producer = Kafka_Producer()
    producer.producer_init()