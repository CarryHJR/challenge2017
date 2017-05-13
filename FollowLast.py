#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-19 14:22:35
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$
import threading
import socket
from rplidar import RPLidar
import numpy as np
import time
import serial
signal = 'start'
flag = True
flagForward = True
flagDist = True


def ReceiveSignal():
    global signal
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建一个socket
    s.connect(('127.0.0.1', 5555))  # 建立连接
    try:
        while True:  # 接受多次数据
            print('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
            signal = s.recv(1024).decode('utf-8')
            print(signal)  # 打印接收到的大写数据
    finally:
        s.close()
        print('error')


SignalThread = threading.Thread(target=ReceiveSignal)
SignalThread.start()
print('the thread of receiving signals is running')

lidar = RPLidar('/dev/ttyUSB0')
info = lidar.get_info()
print(info)
health = lidar.get_health()
print(health)
time.sleep(3)


def measure(scan):
    data = scan
    a = [x[1] for x in data if x[1] > 320 or x[1] < 40]
    b = [x[2] for x in data if x[1] > 320 or x[1] < 40]
    c = []
    j = 0
    for x in b:
        if x > 60 and x < 1500:
            c.append(a[j])
        j = j + 1

    d = [x for x in b if x < 1500]
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
    global flag, signal, flagForward, flagDist
    for i, scan in enumerate(lidar.iter_scans()):
        pos, dist = measure(scan)

        if signal == 'start':
            print('postion:' + str(pos) + '  distance:' + str(dist))
            if dist > 800 and flagDist:
                ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
                ser.write('move straight:300,10000\r\n'.encode())
                ser.close()
                flagForward = False
                flagDist = False
                print(
                    'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff')
            if dist < 700 and flagDist is False:
                ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
                ser.write('stop\r\n'.encode())
                ser.close()
                print(
                    'bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb')
                flagForward = True
                flagDist = True
            if flagForward:
                if pos < -20 and flag:
                    print('rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
                    flag = False

                    ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
                    ser.write('left rotating:9500,10000\r\n'.encode())
                    ser.close()

                if pos > 20 and flag:
                    print('llllllllllllllllllllllllllllllllllll')
                    flag = False

                    ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
                    ser.write('right rotating:9000,10000\r\n'.encode())
                    ser.close()

                if pos > -5 and pos < 5 and flag is False:
                    flag = True
                    print('sssssssssssssssssssssssssssss')

                    ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
                    ser.write('stop\r\n'.encode())
                    ser.close()


finally:
    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()
    ser = serial.Serial(port='/dev/ttyUSB1', baudrate=115200)
    ser.write('stop\r\n'.encode())
    ser.close()
