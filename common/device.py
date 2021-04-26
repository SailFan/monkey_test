# encoding: utf-8
# @Time    : 2021/3/12 9:36 上午
# @Author  : Sail
# @File    : device.py
# @Software: PyCharm
import os
import sys

class Device():

    def __init__(self, default_deviceid = None, default_index = 0):
        self._deviceid = None
        self._default_index = default_index
        self._deviceids = []
        self._default_deviceid=default_deviceid


    def tryConnect(self):
        self.get_deviceid_list()
        if len(self._deviceids)==0:
            return "没有找到连接设备"
        if self._default_deviceid is None:
            if self._default_index < 0 or self._default_index > len(self._deviceids) - 1:
                print('默认连接index超出范围,默认第一个')
                self._default_index = 0
            if len(self._deviceids) >= 1:
                self._deviceid = self._deviceids[self._default_index]

        elif self._default_deviceid in self._deviceids:
            self._deviceid = self._default_deviceid
        else:
            print('没有找到指定连接设备')
        return self._deviceid

    # 获取安卓设备列表
    def get_deviceid_list(self):
        if os.popen("adb version").read()=="":
            sys.exit("没有adb环境")
        ret=os.popen('adb devices').readlines()
        if (len(ret))>2:
            for devicestr in ret:
                if "\tdevice" in devicestr:
                    deviceid = devicestr.split('\t')[0]
                    self._deviceids.append(deviceid)



