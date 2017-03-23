#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-19 13:50:49
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$na
import threading
from selenium import webdriver
import time
import serial

flagPay = False


def Pay():
    driverPay = webdriver.Chrome()
    url = 'https://auth.alipay.com/login/index.htm'
    driverPay.get(url)
    '''
    time.sleep(2)
    name = driverPay.find_element_by_id('J-input-user')
    name.send_keys('15155676576')
    pwd = driverPay.find_element_by_id('password_rsainput')
    pwd.send_keys('hnh7176564')
    '''

    while (driverPay.current_url == url):
        pass

    money = driverPay.find_element_by_xpath('//*[@id="J-assets-balance"]/div[1]/div/div[2]/div/strong/span').text

    while True:
        time.sleep(0.5)
        driverPay.refresh()
        money = driverPay.find_element_by_xpath(
            '//*[@id="J-assets-balance"]/div[1]/div/div[2]/div/strong').text
        if float(money) > float(money):
            break
    global flagPay
    flagPay = True


# pay thread
payThread = threading.Thread(target=Pay)
payThread.start()


driverShop = webdriver.Chrome()
driverShop.get(
    'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/home.html')

# RFID环节
serRFID = serial.Serial('/dev/ttyUSB0', baudrate=115200, timeout = 0.5)
# port = "/dev/ttyUSB2"

goods = set()
print u'串口打开'
while 1:
    line = serRFID.readline().strip()
    if line != '':
        print 'something receive'
        if (line[0], line[-1]) == ('A', '1'):
            goods.add(1)

        if (line[0], line[-1]) == ('L', '1'):
            goods.remove(1)

        if (line[0], line[-1]) == ('A', '2'):
            goods.add(2)

        if (line[0], line[-1]) == ('L', '2'):
            goods.remove(2)

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

    if driverShop.current_url.find('pay') != -1:
        break


while flagPay is False:
    pass

urlSuccess = 'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/success.html'
driverShop.get(urlSuccess)
