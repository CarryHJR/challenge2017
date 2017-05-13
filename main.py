#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-22 04:43:23
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$
import threading
from selenium import webdriver
import time
import serial
import video
import numpy as np
import cv2

line = ''

'''
# the thread of rifd dection starts
def rfid():
    global line
    serRFID = serial.Serial('/dev/ttyUSB2', baudrate=115200, timeout = 0.5)
    while True:
        line = serRFID.readline().strip()


rfidThread = threading.Thread(target=rfid)
rfidThread.start()
print 'rfid thread starts'
'''


# distance thread starts
'''
distance = 20


def dist():
    global distance

    while True:
        # print 'test'
        # serDist.write('start\r\n')
        time.sleep(0.05)
        serDist = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
        distance = serDist.readline().strip()
        print 'read', distance
        serDist.close()




d = threading.Thread(target=dist)
d.start()
'''
# open the serial port of motion
#serMove = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)


# first of all: get home.html
driverShop = webdriver.Chrome()
driverShop.get(
    'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/home.html')

# the list of goods bought
goods = set()


flagPay = False
flagCamshift = False
# the url of webdriver
url = ''

# the thread of pay starts


def Pay():
    driverPay = webdriver.Chrome()
    url = 'https://auth.alipay.com/login/index.htm'
    driverPay.get(url)

    while (driverPay.current_url == url):
        pass

    money1 = driverPay.find_element_by_xpath(
        '//*[@id="J-assets-balance"]/div[1]/div/div[2]/div/strong/span').text

    while True:
        time.sleep(0.5)
        driverPay.refresh()
        money2 = driverPay.find_element_by_xpath(
            '//*[@id="J-assets-balance"]/div[1]/div/div[2]/div/strong').text
        if float(money2) > float(money1):
            global flagPay
            flagPay = True
        money1 = money2


payThread = threading.Thread(target=Pay)
payThread.start()

print 'alipay thread starts'


class App(object):

    def __init__(self):
        # print 'test1'
        # self.ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
        global serMove
        self.ser = serMove
        # self.serDist = serial.Serial(
        #    port='/dev/ttyUSB0', baudrate=115200, timeout=1)
        # print 'test2'
        self.cam = video.create_capture(0)
        ret, self.frame = self.cam.read()
        cv2.namedWindow('camshift')
        cv2.moveWindow('camshift', 0, 0)
        self.x = 0
        self.y = 0
        self.selection = True
        self.flag = True
        self.flagForward = True

    def run(self):
        # i = 0
        while True:
            # time.sleep(0.001)
            # i = i + 1
            ret, self.frame = self.cam.read()
            vis = self.frame.copy()

            hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, np.array((0., 60., 32.)),
                               np.array((180., 255., 255.)))

            if self.selection:
                x0, y0, x1, y1 = (279, 116, 485, 309)
                # print 'x0:%d x1=%d x1=%d y1=%d' % (x0,y0,x1,y1)
                # x0:284 x1=171 x1=437 y1=324
                self.track_window = (x0, y0, x1 - x0, y1 - y0)
                hsv_roi = hsv[y0:y1, x0:x1]
                mask_roi = mask[y0:y1, x0:x1]
                hist = cv2.calcHist([hsv_roi], [0], mask_roi, [16], [0, 180])
                cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
                self.hist = hist.reshape(-1)
                # self.show_hist()

                vis_roi = vis[y0:y1, x0:x1]
                cv2.bitwise_not(vis_roi, vis_roi)
                vis[mask == 0] = 0

            self.selection = None
            # 计算概率分布图
            prob = cv2.calcBackProject([hsv], [0], self.hist, [0, 180], 1)
            prob &= mask
            # 迭代终止条件
            term_crit = (cv2.TERM_CRITERIA_EPS |
                         cv2.TERM_CRITERIA_COUNT, 10, 1)
            track_box, self.track_window = cv2.CamShift(
                prob, self.track_window, term_crit)

            cv2.ellipse(vis, track_box, (0, 0, 255), 2)
            self.x = track_box[0][0]
            self.y = track_box[0][1]

            if self.x - 300 > 70 and self.flag:
                self.flag = False
                self.ser.write('right rotating:12000,10000\r\n')
                # threading.Thread(target=Move().runRight())
                print 'right'

            if self.x - 300 < -70 and self.flag:
                self.flag = False
                self.ser.write('left rotating:12000,10000\r\n')
                # threading.Thread(target=Move().runLeft())
                print 'left'

            if self.x - 300 > -70 and self.x - 300 < 70 and self.flag is False:
                print 'stop'
                self.flag = True
                self.ser.write('stop\r\n')
                # threading.Thread(target=Move().runStop())

            cv2.imshow('camshift', vis)

            ch = 0xFF & cv2.waitKey(5)

            global url
            if url.find('daohanging') != -1:
                break

            if ch == 27:
                break
        cv2.destroyAllWindows()

# RFID环节
serRFID = serial.Serial('/dev/ttyUSB1', baudrate=115200, timeout=0.5)
# port = "/dev/ttyUSB2"


while True:
    global url
    url = driverShop.current_url
    # here , the man click the button "zidongdaohang" OK
    if url.find('introduction2') != -1:
        print 'daohang starts'
        # go straight

        serMove.write('move straight:300,200\r\n')
        serMove.readline().find('Errors')
        while True:
            line = serMove.readline().strip()
            print line
            if line.find('OK') != -1:
                break

        print 'daohang over'
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/introduction3.html')

    # line = serRFID.readline().strip()
    # here, someone throws something OK
    line = ''
    if line != '':
        print 'someone buys', line
        if (line[0], line[-1]) == ('A', '1'):
            goods.add(1)

        if (line[0], line[-1]) == ('L', '1'):
            goods.remove(1)

        if (line[0], line[-1]) == ('A', '2'):
            goods.add(2)

        if (line[0], line[-1]) == ('L', '2'):
            goods.remove(2)

        # man throw somen things

        goodstr = ''
        for x in goods:
            goodstr = goodstr + str(x)

        if goodstr == '':
            driverShop.get(
                'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart.html')

        if goodstr == '1':
            driverShop.get(
                'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart31.html')

        if goodstr == '2':
            driverShop.get(
                'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart32.html')

        if goodstr == '12':
            driverShop.get(
                'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart312.html')

        if goodstr == '21':
            driverShop.get(
                'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart321.html')

    # here, someone pays OK
    if url.find('pay') != -1:
        print 'someone pays'
        flagPay = True
        while flagPay is False:
            pass
        # pay successfully
        urlSuccess = 'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/success.html'
        driverShop.get(urlSuccess)
        # serRFID.write('KILL\r\n')

    # camshift
    if url.find('daohanging') != -1:
        print 'camshift starts'
        flag = True
        while True:
            if flag:
                try:
                    global url
                    url = driverShop.current_url
                    if url.find('daohangend') != -1:
                        break
                    flag = False
                    App().run()

                except Exception, e:
                    print e
                    flag = True
