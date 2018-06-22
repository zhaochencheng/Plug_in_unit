#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 14:26
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Producer_init.py
# @Software: PyCharm
# from pykafka import KafkaClient
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
        #函数作用：向kafka中 (push)写入 消息
        #参数说明：hostname 连接Kafka地址：例：localhost:9092
        #         topic   消息根据Topic进行归类，可以理解为一个队列
        #         msg     要发送的消息
        #兼容 Python2 和 python3
        '''
        if sys.version_info.major == 2:
            #python2 connect Kafka
            from pykafka import KafkaClient
            #链接kafka
            client = KafkaClient(hosts=self.hostname)
            #答应当前kafka中的topics
            print(client.topics)
            Topic = client.topics[self.topic]
            producer = Topic.get_producer()
            producer.produce(self.msg)
            print(self.msg)
            producer.stop()

        elif sys.version_info.major == 3:
            #python3 connect Kafka
            from kafka import KafkaClient, SimpleProducer
            kafka = KafkaClient(self.hostname)
            producer = SimpleProducer(kafka)
            producer.send_messages(self.topic, bytes("%s" % self.msg, encoding="utf-8"))
            print("Published msg -> 'topic:%s'  -> msg:%s" % (self.topic, self.msg))
            # pass

if __name__ == '__main__':
    producer = Kafka_Producer()
    producer.producer_init()
    # msg = get_data("kafka2","producer_msg")
    # print(bytes("%s"%msg,encoding="utf-8"))
    # print(type(msg))
    # print(type(b'[12,"fdsf"]'))
    # msg2 = "%s"%msg
    # print(bytes(msg2,encoding='utf-8'))