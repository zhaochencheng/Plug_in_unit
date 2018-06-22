#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/6/15 14:33
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : function_public.py
# @Software: PyCharm
import sys
import os
import time


def get_data(config_fdir,config_data,config_file="/Config/conf_data.ini"):
    '''
    #
    #函数作用：从参数文件中获取参数值
    #参数说明：config_fdir 需要获取参数的目录名称
    #          config_data 需要获取参数的名称
    #          config_file 参数文件的名称
    #兼容 Python2 和 python3
    '''
    if sys.version_info.major == 2:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "../.."))+ config_file
        config.read(file_path)
        data = config.get(config_fdir, config_data)
        #print(config_data + ": %s" % data)
        return data
    elif sys.version_info.major == 3:
        import configparser
        config = configparser.ConfigParser()
        file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "../.."))+ config_file
        config.read(file_path,encoding='utf-8')
        data = config.get(config_fdir, config_data)
        return data


def set_date(config_fdir,config_data,value_data,config_file="/Config/conf_data.ini"):
    '''
    #函数作用：从参数文件中写入参数值
    #参数说明：config_fdir 需要获取参数的目录名称
    #          config_data 需要获取参数的名称
    #          config_file 参数文件的名称
    #兼容 Python2 和 python3
    '''
    if sys.version_info.major == 2:
        import ConfigParser
        config = ConfigParser.ConfigParser()
        file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "../..")) + config_file
        config.read(file_path)
        config.set(config_fdir,config_data,value_data)
        with open(file_path, 'w+') as f:
            config.write(f)
    elif sys.version_info.major == 3:
        import configparser
        config = configparser.ConfigParser()
        file_path = os.path.abspath(os.path.join(os.path.realpath(__file__), "../..")) + config_file
        config.read(file_path,encoding='utf-8')
        config.set(config_fdir,config_data,value_data)
        with open(file_path, 'w+',encoding='utf-8') as f:
            config.write(f)



if __name__ == '__main__':
    # print(sys.version_info.major)
    import pprint
    print(get_data("kafka","topics"))
    set_date("kafka","rtloest","192.00169")