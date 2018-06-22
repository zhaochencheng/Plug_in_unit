#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 17:26
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Mysql_Client.py
# @Software: PyCharm
import pymysql
import sys
from Plug_in_unit.public_script.function_public import *
# hostip= get_data("mysql","hostip")
# port = get_data("mysql","port")
# username = get_data("mysql","username")
# pwd = get_data("mysql","pwd")
# database = get_data("mysql","database")
#
# db = pymysql.connect(host= hostip,port=int(port),user=username,password=pwd,database=database )
# cursor = db.cursor()
# cursor.execute("select * FROM AdaptMode")
# # data = cursor.fetchone()
# data = cursor.fetchall()
# print(data)
# db.close()

class MySQL():
    #初始化数据
    hostip= get_data("mysql","hostip")
    port = get_data("mysql","port")
    username = get_data("mysql","username")
    pwd = get_data("mysql","pwd")
    database = get_data("mysql","database")
    def Mysql_operate(self,operation):
        '''
        :param operation: connect mysql and operate it
        :return:
        兼容 Python2 and python3
        '''
        if sys.version_info.major == 2:
            #python2 connect mysql
            try:
                db = pymysql.connect(host=self.hostip, port=int(self.port), user=self.username, password=self.pwd, database=self.database)
                cursor = db.cursor()
                cursor.execute(operation)
                db.commit()
                data = cursor.fetchall()
                cursor.close()
                db.close()
                return data
            except Exception as E:
                print(E)
                raise
        elif sys.version_info.major == 3:
            #python3 connect mysql
            try:
                db = pymysql.connect(host=self.hostip, port=int(self.port), user=self.username, password=self.pwd, database=self.database)
                cursor = db.cursor()
                cursor.execute(operation)
                db.commit()
                data = cursor.fetchall()
                print(data)
                cursor.close()
                db.close()
                return data
            except Exception as E:
                print(E)
                raise
if __name__ == '__main__':
    mysql = MySQL()
    mysql.Mysql_operate("SELECT * FROM AdaptInfo WHERE ResID=10;")
    operation = 'update AdaptInfo set ResVersion= 6 where ResID=7;'
    # mysql.Mysql_operate(operation)
    mysql.Mysql_operate("delete from AdaptInfo where ResID = 9 ")
