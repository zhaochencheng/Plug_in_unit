#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/21 17:26
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : Mysql_Client.py
# @Software: PyCharm
import pymysql
from Plug_in_unit.public_script.function_public import *
hostip= get_data("mysql","hostip")
port = get_data("mysql","port")
username = get_data("mysql","username")
pwd = get_data("mysql","pwd")
database = get_data("mysql","database")

db = pymysql.connect(host= hostip,port=int(port),user=username,password=pwd,database=database )
cursor = db.cursor()
cursor.execute("select * FROM AdaptMode")
# data = cursor.fetchone()
data = cursor.fetchall()
print data
db.close()