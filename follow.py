#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import video
import time
import serial
import threading
from pprint import pprint


def camshift():

    cam = video.create_capture(0)
    ret, frame = cam.read()
    cv2.namedWindow('camshift')
    cv2.moveWindow('camshift', 0, 0)
    x = 0
    selection = True
    flag = True
    flagForward = True
    x2 = 0

    while True:
        ret, frame = cam.read()
        vis = frame.copy()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, np.array((0., 60., 32.)),
                           np.array((180., 255., 255.)))
        if selection:
            # initial region
            x0, y0, x1, y1 = (279, 116, 485, 309)
            track_window = (x0, y0, x1 - x0, y1 - y0)
            hsv_roi = hsv[y0:y1, x0:x1]
            mask_roi = mask[y0:y1, x0:x1]
            hist = cv2.calcHist([hsv_roi], [0], mask_roi, [16], [0, 180])
            cv2.normalize(hist, hist, 0, 255, cv2.NORM_MINMAX)
            hist = hist.reshape(-1)
            vis_roi = vis[y0:y1, x0:x1]
            cv2.bitwise_not(vis_roi, vis_roi)
            vis[mask == 0] = 0
        selection = False
        # 计算概率分布图
        prob = cv2.calcBackProject([hsv], [0], hist, [0, 180], 1)
        prob &= mask
        # 迭代终止条件
        term_crit = (cv2.TERM_CRITERIA_EPS |
                     cv2.TERM_CRITERIA_COUNT, 10, 1)
        track_box, track_window = cv2.CamShift(
            prob, track_window, term_crit)
        # pprint(track_window)
        # pprint(track_box)
        cv2.ellipse(vis, track_box, (0, 0, 255), 2)
        x = track_box[0][0]
        print x
        if x - 300 > 70 and flag:
            flag = False
            # ser.write('right rotating:12000,10000\r\n')
            # threading.Thread(target=Move().runRight())
            print 'rrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr'

        if x - 300 < -70 and flag:
            flag = False
            # ser.write('left rotating:12000,10000\r\n')
            # threading.Thread(target=Move().runLeft())
            print 'lllllllllllllllllllllllllllllllllllllllllllllllllllllll'

        if x - 300 > -70 and x - 300 < 70 and flag is False and flagForward:
            print 'ssssssssssssssssssssssssssssssssssssssssssssssssssssssss'
            flag = True
            # ser.write('stop\r\n')
            # threading.Thread(target=Move().runStop())
        cv2.imshow('camshift', vis)
        ch = 0xFF & cv2.waitKey(5)
        if ch == 27:
            break
    cv2.destroyAllWindows()


def follow():
    flag = True
    while True:
        if flag is True:
            try:
                flag = False
                camshift()
                break
            except Exception, e:
                print e
                flag = True


followThread = threading.Thread(target=follow)
followThread.start()
