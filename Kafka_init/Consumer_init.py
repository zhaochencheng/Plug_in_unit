#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 14:26
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Consumer_init.py
# @Software: PyCharm
# from pykafka import KafkaClient
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
        消费者 向kafka中 pull 消息
        #函数作用：向kafka中 (pull)拉取 消息
        #参数说明：hostname 连接Kafka地址：例：localhost:9092
        #         topic   消息根据Topic进行归类，可以理解为一个队列
        #         groupID  一个字符串用来指示一组consumer所在的组。相同的groupID表示在一个组里。相同的groupID消费记录offset时，记录的是同一个offset
        #         zookeeper_hostname =
        #兼容 Python2 和 python3
        '''
        if sys.version_info.major == 2:
            #python2 connect kafka
            from pykafka import KafkaClient
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
            #python3 connect kafka
            from kafka import KafkaConsumer
            consumer = KafkaConsumer(self.topic,group_id=self.groupID,bootstrap_servers=[self.hostname])
            print("consumer start")
            for message in consumer:
                print("Consumed Msg -> '%s' on Topic -> '%s' with Offset -> %d" %(message.value.decode('utf-8'), message.topic, message.offset))
            print("consumer close")
            consumer.close()
            pass
if __name__ == '__main__':
    consumer = Kafka_consumer()
    consumer.Consumer_Init()