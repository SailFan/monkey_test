import os, sys, time
import subprocess

'''设备操作类'''
'''teky'''
class DeviceCtrl():

    def __init__(self, deviceid):
        self.deviceid = deviceid
        self.width = 0
        self.height = 0
        self.judge_device()

    def judge_device(self):
        cmd="adb devices -l"
        rt = os.popen(cmd).read()
        if not "HW" in rt:
            print("华为手机调试的，其他手机可能会有些不兼容，应该问题不大，自己改改。")



    def adbpush(self, localfile, despath):
        '''adb push'''
        cmd = 'adb -s ' + self.deviceid + ' push ' + localfile + ' ' + despath
        rt = os.popen(cmd).read()
        if not "pushed" in rt:
            print(rt)
        
    def adbpull(self, mobilefil, despath):
        '''adb pull'''
        cmd = 'adb -s ' + self.deviceid + ' pull ' + mobilefil + ' ' + despath
        #print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if not "pulled" in rt:
            print(rt)



    def dumpUI_compressed(self, xmlpath=None):
        '''获取uiautomator dump'''
        cmd = 'adb -s ' + self.deviceid + ' shell uiautomator dump --compressed /sdcard/tmp/uidump.xml'
        rt = os.popen(cmd).read()
        if rt.find('UI hierchary dumped')>=0:
            if xmlpath:
                self.adbpull('/sdcard/tmp/uidump.xml',xmlpath)
                return xmlpath
            else:
                self.adbpull('/sdcard/tmp/uidump.xml', self.deviceid + '_uidump.xml')
                return sys.path[0] + '/'+ self.deviceid +'_uidump.xml'
        else:
            print('dump 失败:' + rt)
            return None
    
    def dumpUI(self, xmlpath=None):
        '''获取uiautomator dump'''
        cmd = 'adb -s ' + self.deviceid + ' shell uiautomator dump  /sdcard/tmp/tmp/uidump.xml'
        #print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if rt.find('UI hierchary dumped')>=0:
            if xmlpath:
                self.adbpull('/sdcard/tmp/uidump.xml',xmlpath)
                return xmlpath
            else:
                self.adbpull('/sdcard/tmp/uidump.xml', self.deviceid + '_uidump.xml')
                return sys.path[0] + '/'+ self.deviceid +'_uidump.xml'
        else:
            print('dump 失败:' + rt)
            return None
    
    def screenshot(self, filepath):
        '''获取uiautomator dump'''
        try:
            cmd = 'adb -s ' + self.deviceid + ' shell screencap -p /data/local/tmp/screen.png'
            #print('命令:' + cmd)
            os.popen(cmd)
            time.sleep(2)
            self.adbpull('data/local/tmp/screen.png', filepath)#卡死?
            time.sleep(2)
        except Exception as e:
            print(e)
        finally:
            return

    def stopapp(self, package):
        cmd = 'adb -s ' + self.deviceid + ' shell am force-stop ' + package
        print('命令:' + cmd)
        os.popen(cmd).read()
        time.sleep(3)#太快应用起不来

    def startapp(self, package, activity):
        '''启动一个应用 com.android.filemanager/.FileManagerActivity'''
        cmd = 'adb -s ' + self.deviceid + ' shell am start -n ' + package + '/' + activity
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        print(rt)
        if rt.find('Starting:')>=0:
            time.sleep(2)#等待应用启动
            return True
        else:
            print('启动失败,检查包名和Activity参数')
            return False
        
    def trywakeup(self):
        '''执行唤醒返回TRUE，原来是点亮的返回FAlSE'''

        cmd = 'adb -s ' + self.deviceid + ' shell dumpsys window policy | grep \"mScreenOnFully\" '
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if rt.find('mScreenOnFully=false')>=0:#锁屏 按下power点亮
            self.presspower()#KEYCODE_POWER
            print('点亮屏幕')
            return True
        else:
            return False

    def trywakeoff(self):
        '''执行熄灭返回TRUE，原来是熄灭的返回FAlSE'''
        cmd = 'adb -s ' + self.deviceid + ' shell dumpsys window policy | grep \"mScreenOnFully\" '
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if rt.find('mScreenOnFully=true')>=0:#亮屏 按下power点亮
            self.presspower()#KEYCODE_POWER
            print('熄灭屏幕')
            return True
        else:
            return False
    
    def presshome(self):
        self.sendkeycode(KeyCodes.KEYCODE_HOME)
        time.sleep(1)
    
    def pressback(self):
        self.sendkeycode(KeyCodes.KEYCODE_BACK)
        time.sleep(1)

    def presspower(self):
        self.sendkeycode(KeyCodes.KEYCODE_POWER)
        time.sleep(1)


    # def wakeup(self):
    #     '''点亮并解锁'''
    #     #自动化点亮并滑动解锁
    #     self.getdisplaysize()
    #     self.trywakeup()
    #     self.set_screen_off_timeout(10)
    #     time.sleep(1)
    #     self.unlock_by_swipe()
    #     self.presshome()


    def wakeupme(self):
        """解锁屏幕并且返回首页"""
        self.trywakeup()
        time.sleep(1)
        cmd = 'adb -s ' + self.deviceid + ' shell input keyevent 82'
        rt = os.popen(cmd).read()
        time.sleep(1)
        self.presshome()


    def getdisplaysize(self):
        '''得到屏幕分辨率'''
        cmd = 'adb -s ' + self.deviceid + ' shell wm size'
        print('命令:' + cmd)
        rt = os.popen(cmd).read()

        if rt.find('size:')>0:
            rt = rt.split(': ')
            rt = rt[1].split('x')
            self.width = int(rt[0])
            self.height = int(rt[1])
    
    def unlock_by_swipe(self):
        '''常规向上滑动解锁'''
        x1 = x2 = str(self.width/2)
        y1 = str(self.height/2 + self.height/3)
        y2 = str(self.height/2 - self.height/3)
        cmd = 'adb -s ' + self.deviceid + ' shell input swipe ' + x1 + ' '+ y1 + ' ' + x2 + ' ' + y2 + ' 200'
        print('命令:' + cmd)
        os.popen(cmd)

    def swipe_up(self):
        '''常规向上滑动'''
        x1 = x2 = str(self.width/2)
        y1 = str(self.height/2 + self.height/8)
        y2 = str(self.height/2 - self.height/8)
        cmd = 'adb -s ' + self.deviceid + ' shell input swipe ' + x1 + ' '+ y1 + ' ' + x2 + ' ' + y2 + ' 300'
        os.popen(cmd)
        time.sleep(1)
    
    def swipe_down(self):
        '''常规向下滑动'''
        x1 = x2 = str(self.width/2)
        y1 = str(self.height/2 - self.height/8)
        y2 = str(self.height/2 + self.height/8)
        cmd = 'adb -s ' + self.deviceid + ' shell input swipe ' + x1 + ' '+ y1 + ' ' + x2 + ' ' + y2 + ' 300'
        os.popen(cmd)
        time.sleep(1)

    def click_tuplexy(self, tuplexy):
        '''点击坐标'''
        if not tuplexy:
            return
        cmd = 'adb -s ' + self.deviceid + ' shell input tap ' + str(tuplexy[0]) + ' '+ str(tuplexy[1])
        #print('命令:' + cmd)
        os.popen(cmd)
        time.sleep(1)

    def click(self, x, y):
        '''点击坐标'''
        cmd = 'adb -s ' + self.deviceid + ' shell input tap ' + str(x) + ' '+ str(y)
        os.popen(cmd)
        time.sleep(1)

    def waitfordevice(self):
        '''重启后等待adb连接'''
        cmd = 'adb -s ' + self.deviceid + ' shell dumpsys window policy | grep \"mScreenOnFully\" '
        print('命令:' + cmd)
        rt = os.popen(cmd).read()
        if rt.find('mScreenOnFully=false')>=0:
            print('连接成功')
            return True
        else:
            print('未连接成功')
            time.sleep(10)
            return self.waitfordevice()
 
    def sendbroadcast(self, file_path):
        '''广播'''
        cmd = 'adb -s ' + self.deviceid + ' shell am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d '+ file_path
        print('命令:' + cmd)
        os.popen(cmd)
        
    def input_text(self, text):
        '''输入文字'''
        cmd = 'adb -s ' + self.deviceid + ' shell input text '+ text
        print('命令:' + cmd)
        os.popen(cmd)
    
    def getversion(self):
        '''获取版本号'''
        cmd = 'adb -s ' + self.deviceid + ' shell getprop ro.build.version.release'
        print('命令:' + cmd)
        return os.popen(cmd).read().strip()

    def getproductname(self):
        '''获取项目名称'''
        cmd = 'adb -s ' + self.deviceid + ' shell getprop ro.product.name'
        print('命令:' + cmd)
        return os.popen(cmd).read().strip()
    
    def sendkeycode(self, keycode):
        '''模拟按键'''
        cmd = 'adb -s ' + self.deviceid + ' shell input keyevent ' + str(keycode)
        os.popen(cmd)
        #print('命令:' + cmd)

    def get_topfullactivity(self):
        '''获取最上方Activity'''
        cmd = 'adb -s ' + self.deviceid + ' shell dumpsys activity | grep mResumedActivity '
        rt = os.popen(cmd).read()
        if rt.find('mResumedActivity: ActivityRecord')>=0:
            rts = rt.split(' ')
            return rts[7]
        else:
            return None
    
    def set_screen_off_timeout(self, minute):
        '''设置锁屏时间'''
        cmd = 'adb -s ' + self.deviceid + ' shell settings put system screen_off_timeout ' + str(minute*60000)
        os.popen(cmd).read()
        print('设置锁屏时间' + str(minute) + '分钟')



#定义keycode信息
class KeyCodes():
    KEYCODE_MENU = 1
    KEYCODE_HOME = 3
    KEYCODE_BACK = 4
    KEYCODE_VOLUME_UP = 24
    KEYCODE_VOLUME_DOWN = 25
    KEYCODE_POWER = 26



