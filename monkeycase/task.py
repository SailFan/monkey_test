# encoding: utf-8
# @Time    : 2021/3/12 1:18 下午
# @Author  : Sail
# @File    : task.py
# @Software: PyCharm
import unittest

from common.HTMLTestRunner import HTMLTestRunner

from common.devicectrl import DeviceCtrl
from monkeycase.MonkeyTestCase import MonkeyTestCase


class Task():
    def __init__(self, apkversion,deviceid,devctrl,reportfile):
        self.report_title = 'monkey测试报告'
        self.apkversion = apkversion
        self.deviceid=deviceid
        self.devctrl=devctrl
        self.reportfile=reportfile

    def start(self):
        self.report_des = '模块版本:' + self.apkversion
        suite=unittest.TestSuite()
        self.devctrl.wakeupme()
        suite.addTest(MonkeyTestCase("test_monkey"))
        with open(self.reportfile,"wb") as f:
            return HTMLTestRunner(stream=f,title=self.report_title,description=self.report_des,verbosity=2).run(suite)
