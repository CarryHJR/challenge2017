#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-14 21:00:01
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$

from rplidar import RPLidar
from pprint import pprint
import numpy as np
import os
import time
import socket
from pprint import pprint
import json


# class Move(object):

#     def __init__(self):
#         self.ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)

#     def runRight(self):
#         try:
#             self.ser.write('right rotating:12000,10000\r\n')
#             self.ser.close()
#         except Exception, e:
#             print e
#         print 'turn right'

#     def runLeft(self):
#         try:
#             self.ser.write('left rotating:12000,10000\r\n')
#             self.ser.close()
#         except Exception, e:
#             print e
#         print 'turn left'

#     def runStop(self):
#         try:
#             self.ser.write('stop\r\n')
#             self.ser.close()
#         except Exception, e:
#             print e
#         print 'turn stop'

#     def runStraight(self):
#         try:
#             self.ser.write('move back:250,30000\r\n')
#             self.ser.close()
#         except Exception, e:
#             print e
#         print 'gor straight'


lidar = RPLidar('/dev/ttyUSB0')
info = lidar.get_info()
print(info)
health = lidar.get_health()
print(health)


time.sleep(3)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个socket
s.connect(('127.0.0.1', 5555))


def measure(scan):
    data = scan
    s.send(json.dumps(data).encode())
    # pprint(scan)
    a = [x[1] for x in data if x[1] > 320 or x[1] < 40]
    b = [x[2] for x in data if x[1] > 320 or x[1] < 40]
    c = []
    j = 0
    for x in b:
        if x < 1000:
            c.append(a[j])
        j = j + 1

    d = [x for x in b if x < 1000]
    if d == []:
        return 0, 0
    d.remove(max(d))
    c1 = [x - 360 for x in c if x > 300]
    c2 = [x for x in c if x < 200]
    c2.extend(c1)
    c2.sort()
    # print(b)
    pos = c2[0] + c2[-1]
    # print(pos)
    return pos, np.mean(d)


try:
    for i, scan in enumerate(lidar.iter_scans()):
        pos, dist = measure(scan)
        print('postion:' + str(pos) + '  distance:' + str(dist))
        # if position <
except Exception as e:
    print(e)
finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    s.send(b'quit')
    s.close()
