import base64
from http import client
import time
import socket
# pure-python-adb loading
# pip install -U pure-python-adb
from ppadb.client import Client as AdbClient
# pip install psutil
import psutil
# pip install pytesseract
import pytesseract
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

for proc in psutil.process_iter():
    processName=proc.name()
    processID=proc.pid

class MyWindow(QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.scriptworker = None
        self.captureworker = None
        self.discordworker = None
        self.firstMacro = True
        self.isRun = False
        self.firstMacro = True
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

        self.comboBox.addItem("군수받기")
        self.comboBox.addItem("스크립트제작")
        self.comboBox.addItem("test1")
        self.comboBox.addItem("test2")
        self.comboBox.addItem("test3")
        self.comboBox.addItem("test4")

        # 연결 콤보박스
        devi = serchDivice()
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
        print("sex")

    def onStopClicked(self):
        txt = "sas"
        self.textInputTB1("중지합니다.")
    def onAdbClicked(self):
        ads = self.comboBox_2.currentIndex()
        connect(ads)
        devi = self.comboBox_2.currentText()
        self.textInputTB1(f'Connected to {devi}')

    def onCapClicked(self):
        capture()

    def onCapcv2Clicked(self):
        captureCv2()


    def onTest1Clicked(self):
        global device
        image_byte_array = device.screencap()
        # convert the byte array to a numpy array (RGB)
        image = cv2.imdecode(np.frombuffer(bytes(image_byte_array), np.uint8), cv2.IMREAD_COLOR)
        dst = image.copy()
        #print(dst)
        jin = dst[15:40, 393:493].copy()
        jtan = dst[15:40, 533:633].copy()
        jsik = dst[15:40, 676:776].copy()
        jbu = dst[15:40, 820:920].copy()
        cv2.imwrite('img/tempin.png', jin)
        cv2.imwrite('img/temptan.png', jtan)
        cv2.imwrite('img/tempsik.png', jsik)
        cv2.imwrite('img/tempbu.png', jbu)
        jin = cv2.imread('img/tempin.png', cv2.IMREAD_COLOR)
        jtan = cv2.imread('img/temptan.png', cv2.IMREAD_COLOR)
        jsik = cv2.imread('img/tempsik.png', cv2.IMREAD_COLOR)
        jbu = cv2.imread('img/tempbu.png', cv2.IMREAD_COLOR)
        rgb_image = cv2.cvtColor(jin, cv2.COLOR_BGR2RGB)
        text = pytesseract.image_to_string(rgb_image, lang='kor+eng')
        print(text)


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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindow = MyWindow()
    myWindow.show()
    app.exec_()