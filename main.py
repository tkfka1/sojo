import base64
from http import client
import time
import socket
# pure-python-adb loading
# pip install -U pure-python-adb
import schedule as schedule
from ppadb.client import Client as AdbClient
# pip install psutil
import psutil
import distutils
import os
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
import cv2
import numpy as np
# import win32gui
# import win32api
from PIL import ImageGrab, Image
# import serial.tools.list_ports
# import threading
# import serial
# import struct
import sys
import random

# import asyncio
# import discord
# from discord.ext import commands
# import time
# import schedule
# import tensorflow as tf
# import configparser

form_class = uic.loadUiType("mainWindow.ui")[0]

applay = None
device = None
caplil = 0.1

def connect(n):
    global applay
    global device
    applay = AdbClient(host="127.0.0.1", port=5037) # Default is "127.0.0.1" and 5037
    devices = applay.devices()
    if len(devices) == 0:
        print('No devices')
        quit()
    print(devices)
    device = devices[n]

def serchDivice():
    os.system('cd {}'.format(os.getcwd()))
    # os.chdir("platform-tools")
    output = os.popen('adb devices').read()
    x = output.splitlines()
    devs = []
    for i in range(len(x)-1):
        if x[i][0] == "e":
            temp = x[i][0:13]
            devs.append(temp)
    return devs

def capture():
    global device
    result = device.screencap()
    t = time.strftime('%Y-%m-%d-%M-%S', time.localtime(time.time()))
    with open(f"img/{t}.png", "wb") as fp:
        fp.write(result)

def captureCv2():
    global device
    image_byte_array = device.screencap()
    # convert the byte array to a numpy array (RGB)
    image = cv2.imdecode(np.frombuffer(bytes(image_byte_array), np.uint8), cv2.IMREAD_COLOR)

    cv2.imshow('my image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def captureMain():
    global device
    image_byte_array = device.screencap()
    image = cv2.imdecode(np.frombuffer(bytes(image_byte_array), np.uint8), cv2.IMREAD_COLOR)
    return image

def click(x,y):
    global device
    cmd = "input touchscreen tap " + str(x) + " " + str(y)
    device.shell(cmd)

def clickRand(x, y, dx, dy):
    global device
    newy = y
    xx = random.randint(x, x + dx)
    yy = random.randint(newy, newy + dy)
    cmd = "input touchscreen tap " + str(xx) + " " + str(yy)
    device.shell(cmd)


def clickSwipe(cor):
    global device
    newy = cor[1]
    xx = random.randint(cor[0], cor[0] + cor[2])
    yy = random.randint(newy, newy + cor[3])
    cmd = "input swipe " + str(xx) + " " + str(yy) + " " + str(xx) + " " + str(yy) + " " + str(random.randint(54,178)) #지연 시간 단위는 ms
    device.shell(cmd)

def packageSerch():
    global device
    cmd = "pm list packages -f"
    print(device.shell(cmd))


def startSojo():
    global device
    print("test1")
    cmd = "am start -n kr.txwy.and.snqx/com.txwy.passport.model.MainActivity"
    print(device.shell(cmd))


class Capture:

    supervisor0 = cv2.imread('img/supervisor0.png', cv2.IMREAD_COLOR)
    decision = cv2.imread('img/decision.png', cv2.IMREAD_COLOR)

    def compare(self, img, bbox, what):
        if not bbox[3] == 0:
            img = img[bbox[1]:bbox[3], bbox[0]:bbox[2]]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        res_pos = cv2.matchTemplate((cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)), what,
                                     cv2.TM_CCOEFF_NORMED)
        con_pos = res_pos.max()
        loc_pos = np.where(res_pos == con_pos)
        # cv2.imwrite('img/temp.png', img)
        print(loc_pos[1][0], loc_pos[0][0])
        print(con_pos)
        if con_pos > 0.95:
            return loc_pos[1][0], loc_pos[0][0], 1
        else:
            return 0,0,0








for proc in psutil.process_iter():
    processName=proc.name()
    processID=proc.pid

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.captureworker = None
        self.connectAnd = True
        self.isRun = False
        self.setupUi(self)
        self.mainBtn1.clicked.connect(self.onStartClicked)  # 시작
        self.mainBtn2.clicked.connect(self.onStopClicked)  # 중지
        self.mainBtn3.clicked.connect(self.onAdbClicked)  # adb연결
        # self.comboBox_2.currentIndexChanged.connect(self.conChanged) # 연결콤보박스 핸들러
        self.capBtn.clicked.connect(self.onCapClicked)  # 캡쳐하기
        self.capBtncv2.clicked.connect(self.onCapcv2Clicked)  # 캡쳐하기
        self.testBtn1.clicked.connect(self.onTest1Clicked)  # test1
        self.testBtn2.clicked.connect(self.onTest2Clicked)  # test2
        self.testBtn3.clicked.connect(self.onTest3Clicked)  # test3
        self.doubleSpinBoxLil.valueChanged.connect(self.lil_changed)  # 캡쳐주기 변경

        self.comboBox.addItem("군수받기")
        self.comboBox.addItem("스크립트제작")
        self.comboBox.addItem("test1")
        self.comboBox.addItem("test2")
        self.comboBox.addItem("test3")
        self.comboBox.addItem("test4")

        self.label_status.setText("중지")

        # 연결 콤보박스
        devi = serchDivice()
        if devi == []:
            txt = "안드로이드가 실행중이지 않습니다."
            self.mainTB1.append(txt)
            scrollbar = self.mainTB1.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
            txt = "안드로이드를 실행한후 다시실행해주세요."
            self.mainTB1.append(txt)
            scrollbar = self.mainTB1.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        else:
            for i in devi:
                self.comboBox_2.addItem(i)


    # 텍스트 넣어주기 tI
    @pyqtSlot(str)
    def textInputTB1(self, txt):
        # print("텍스트 넣어주기 함수")
        self.mainTB1.append(txt)
        scrollbar = self.mainTB1.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())


    # 시작버튼
    def onStartClicked(self):
        if self.connectAnd: self.textInputTB1("안드로이드연결이없습니다."); return
        if self.isRun: self.textInputTB1("이미 실행중입니다."); return
        else:
            self.label_status.setText("정상동작중")
            self.label_status.setStyleSheet(
                "color: #41E881; border-style: solid; border-width: 2px; border-color: #67E841; border-radius: 10px; ")
            self.startMacro()

    def onStopClicked(self):
        self.textInputTB1("중지합니다.")
        try:
            self.captureworker.pause()
        except:
            self.textInputTB1("캡쳐 쓰레드가 실행중이지 않습니다.")
            # return
        self.isRun = False
    def onAdbClicked(self):
        ads = self.comboBox_2.currentIndex()
        connect(ads)
        devi = self.comboBox_2.currentText()
        self.textInputTB1(f'Connected to {devi}')
        self.connectAnd = False

    def onCapClicked(self):
        capture()

    def onCapcv2Clicked(self):
        captureCv2()

    def onTest1Clicked(self):
        asd = captureMain()
        res = asd[:]
        bbox = [497,438,622,487]
        Capture.compare(self, res, bbox,Capture.decision)
        print("얏다")



    def onTest2Clicked(self):
        global device
        print("test1")
        cmd = "pm dump kr.txwy.and.snqx"
        print(device.shell(cmd))

    def onTest3Clicked(self):
        global device
        print("test1")
        cmd = "am start -n kr.txwy.and.snqx/com.txwy.passport.model.MainActivity"
        print(device.shell(cmd))
    def lil_changed(self):
        global caplil
        caplil = round(self.doubleSpinBoxLil.value(), 2)
    def closeEvent(self, event):
        quit_msg = "종료하시겠습니까??"
        reply = QMessageBox.question(self, '매크로 종료', quit_msg, QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            try:
                event.accept()
            except:
                event.accept()
        else:
            event.ignore()

    ### 기본 시작 매크로###
    def startMacro(self):
        self.textInputTB1("시작합니다.")
        self.isRun = True
        self.captureworker = CaptureWorker()
        self.captureworker.start()
        self.captureworker.textInputTB1.connect(self.textInputTB1)


# 기본 워커
class CaptureWorker(QThread):
    textInputTB1 = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.starttime = 0
        self.scripti = None
        self.running = True
        self.tempimg = None

    def run(self):
        def myloce():
            self.tempimg = captureMain()
            bbox = [780, 576, 923, 628]
            print("sex")
            
            res = Capture.compare(self, self.tempimg, bbox, Capture.supervisor0)
            if res[2] == 1:
                print("군수맞았다")
                x,y,dx,dy = 847,596,20,14
                clickRand(x,y,dx,dy)
                print("눌렀다")
                time.sleep(1)
            else:
                print("군수아닌가벼")
                time.sleep(3)
            self.tempimg = captureMain()
            bbox = [497,438,622,487]
            res = Capture.compare(self, self.tempimg, bbox, Capture.decision)
            if res[2] == 1:
                print("결정맞았다")
                x,y,dx,dy = 557,461,20,20
                clickRand(x,y,dx,dy)
                print("눌렀다")
                time.sleep(30)
            else:
                print("결정아닌가벼")
                time.sleep(30)

        job1 = schedule.every(caplil).seconds.do(myloce)
        while self.running:
            schedule.run_pending()
            time.sleep(caplil)
        else:
            schedule.cancel_job(job1)
    def resume(self):
        self.running = True
    def pause(self):
        self.running = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()