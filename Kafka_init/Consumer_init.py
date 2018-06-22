#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 14:26
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Consumer_init.py
# @Software: PyCharm
from pykafka import KafkaClient
import sys
from Plug_in_unit.public_script.function_public import *
import logging as log
log.basicConfig(level=log.DEBUG)

class Kafka_consumer():
    #初始化数据
    hostname= get_data("kafka2","hostname")
    topic = get_data("kafka2","topics")
    groupID = get_data("kafka2","groupid")
    zookeeper_hostname = get_data("kafka2","zookeeper_ip")

    def Consumer_Init(self):
        '''
        消费者 向kafka中 pull 数据
        '''
        if sys.version_info.major == 2:
            client = KafkaClient(hosts=self.hostname)
            print(client.topics)
            Topic = client.topics[self.topic]
            balanced_consumer = Topic.get_balanced_consumer(
                consumer_group=self.groupID,
                auto_commit_enable=True,#设置为False的时候不需要添加consumer_group，直接连接topic即可取到消息
                zookeeper_connect=self.zookeeper_hostname
            )
            for message in balanced_consumer:
                if message is not None:
                    print(message.offset,message.value)
        elif sys.version_info.major == 3:
            pass
if __name__ == '__main__':
    consumer = Kafka_consumer()
    consumer.Consumer_Init()