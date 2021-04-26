import os
import sys
import unittest
from datetime import datetime
from configobj import ConfigObj

from common.HTMLTestRunner import HTMLTestRunner
from common.device import Device
from common.devicectrl import DeviceCtrl
from monkeycase.MonkeyTestCase import MonkeyTestCase
from monkeycase.task import Task

v_version="v0.19.5.5"



def print_version():
    print(v_version)


def print_help():
    print_version()
    print('调用示例:python start.py -c config')
    print('自动获取连接手机的项目名称和版本名称 deviceid')


def createfolder():
    screen_save_path=sys.path[0]+'/screenshots/'
    reports_path = sys.path[0] + '/reports/'
    monkey_path = sys.path[0] + '/monkeylogs/'



    if not os.path.exists(screen_save_path):
        os.makedirs(screen_save_path)


    if not os.path.exists(reports_path):
        os.makedirs(reports_path)

    if not os.path.exists(monkey_path):
        os.makedirs(monkey_path)

    retportname = deviceid + datetime.now().strftime('%Y_%m_%d_%H_%M_%S') + '.html'
    reportfile = reports_path + retportname

    return (retportname,reportfile)

if __name__ == '__main__':

    inipath=sys.path[0]+"/"+"config.ini"
    config = ConfigObj(inipath, encoding='UTF8')
    author = config["config"]["author"]
    version = config["config"]["version"]
    modular = config["config"]["modular"]
    debug = config["config"]["debug"]


    if not all((author,version,modular,debug)):
        sys.exit("配置文件中都为必填项")
    dev = Device()
    deviceid = dev.tryConnect()
    if deviceid is None:
        sys.exit("没有找到连接手机")
    else:
        devctrl=DeviceCtrl(deviceid)
        version=devctrl.getversion()
        productname = devctrl.getproductname()
        retportname, reportfile = createfolder()
        test_start_time=datetime.now()
        report_des = '模块版本:' + version
        task=Task(apkversion=version,deviceid=deviceid,devctrl=devctrl,reportfile=reportfile)
        task.start()







