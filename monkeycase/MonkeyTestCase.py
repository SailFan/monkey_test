# coding=utf-8
import subprocess
import sys
import time
import unittest

from configobj import ConfigObj

from common.device import Device
from common.devicectrl import DeviceCtrl


class MonkeyTestCase(unittest.TestCase):

    # def setUp(self) -> None:
    #     dev = Device()
    #     self.deviceid=dev.tryConnect()
    #     cmd = f"adb -s {self.deviceid} logcat -v time"
    #     logcatname = sys.path[0] + "/logcat/" + self.deviceid + time.strftime("%Y_%m_%d_%H_%M_%S",
    #                                                                           time.localtime()) + ".txt"
    #     self.logcat_ps = None
    #     with open(logcatname, "w", encoding="utf-8") as f:
    #         f.write(cmd + '\r\n')
    #         f.write("同步logcat日志开始" + '\r\n')
    #         self.logcat_ps = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
    #                                           stderr=subprocess.STDOUT)
    #
    #         while True:
    #             data = bytes.decode(self.logcat_ps.stdout.readline())
    #             f.write(data)
    #
    #
    # def tearDown(self) -> None:
    #     self.logcat_ps.stdout.close()


    def test_monkey(self):
        dev = Device()
        deviceid = dev.tryConnect()
        cmd = f"adb -s {deviceid} logcat -v time"
        testcmd = 'adb -s TPG4C18528008611 shell monkey -p com.che.truckhome.speed  --pct-touch 100  --ignore-crashes --ignore-timeouts --monitor-native-crashes  --throttle 100 -s 1234  -v-v-v 500'
        try:
            logfilename = sys.path[0] + "/monkeylogs/" + deviceid + time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime()) + ".txt"
            logcatname = sys.path[0] + "/logcat/" + deviceid + time.strftime("%Y_%m_%d_%H_%M_%S",time.localtime()) + ".txt"
            with open(logfilename, "w", encoding="utf-8") as f:
                f.write(testcmd + '\r\n')
                ps = subprocess.Popen(testcmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=subprocess.STDOUT)
                rt = True
                while rt:
                    data = bytes.decode(ps.stdout.readline())
                    f.write(data)
                    if "Monkey finished" in data:
                        rt = False
                        f.write("monkey 执行结束了")
                        ps.stdout.close()
        except Exception as e:
            print(e)
