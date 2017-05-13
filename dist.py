#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-27 19:16:06
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$
import time
import serial
import threading
import math


class Move(object):

    def __init__(self):
        self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

    def runRight(self):
        try:
            self.ser.write('right rotating:12000,10000\r\n')
            self.ser.close()
        except Exception, e:
            print e
        print 'turn right'

    def runLeft(self):
        try:
            self.ser.write('left rotating:12000,10000\r\n')
            self.ser.close()
        except Exception, e:
            print e
        print 'turn left'

    def runStop(self):
        try:
            self.ser.write('stop\r\n')
            self.ser.close()
        except Exception, e:
            print e
        print 'turn stop'

    def runStraight(self):
        try:
            self.ser.write('move back:250,30000\r\n')
            self.ser.close()
        except Exception, e:
            print e
        print 'gor straight'


def dist():
    d1 = 200
    d2 = 23
    flagForward = False
    serDist = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
    while True:
        time.sleep(0.01)

        d1 = serDist.readline().strip()
        if math.fabs(float(d2) - float(d1)) > 15 and d1 > 50:
            d1 = d2
        else:
            d2 = d1
        print 'read', d1
        #serDist.close()
        if float(d1) > 50 and float(d1) < 200 and flagForward:
            print '333333333333333333333333333'
            flagForward = False
            # print 'go straight'
            Move().runStraight()

        if float(d1) > 15 and float(d1) < 30 and flagForward is False:
            flagForward = True
            print '666666666666666666666666666'
            Move().runStop()


distThread = threading.Thread(target=dist)
distThread.start()
