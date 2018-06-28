# -*- coding: utf-8 -*-
# @Time    : 2018/6/28 13:38
# @Author  : zhaochencheng
# @Email   : 907779487@qq.com
# @File    : run_all.py
# @Software: PyCharm
import HTMLTestRunner
import os
import unittest
try:
    # 用例路径
    # case_path = os.path.join(os.getcwd(), "test_MSG")
    case_path = os.path.join(os.getcwd(), "Use_case")
    # 报告存放路径
    report_path = os.path.join(os.getcwd(), "test_report")
    # html报告文件
    report_abspath = os.path.join(
        report_path, "test.html")

    # 遍历case_path目录下；批量执行test_用例
    discover = unittest.defaultTestLoader.discover(case_path,
                                                    pattern="test_demo.py",
                                                    top_level_dir=None)
    # #单个执行用例
    # suit = unittest.TestSuite()
    # suit.addTest(Switch("test_switch"))
    # time.sleep(1)
    # suit.addTest(AP_Poe("test_AP_poe"))
    fp = open(report_abspath, "wb")
    #html报告格式 一
    # runner = HTMLTestRunnerXL.HTMLTestRunner(stream=fp,
    #                                        title=u'自动化测试报告,测试结果如下：',
    #                                        description=u'用例执行情况：')
    #Html报告格式 二
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,
                                           title=u'自动化测试报告,测试结果如下：',
                                           description=u'用例执行情况：')
    # 调用add_case函数返回值
    runner.run(discover)  #执行用例
    # runner.run(suit)
    fp.close()

    #调用邮件发送，自动发送邮件
    # file = Search_testReport(report_path)
    # send_email(file)
except Exception as err:
    print(err)