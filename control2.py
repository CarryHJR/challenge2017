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
    name = driverPay.find_element_by_id('J-input-user')
    name.send_keys('15155676576')
    pwd = driverPay.find_element_by_id('password_input')
    pwd.send_keys('hnh7176564')

    while (driverPay.current_url == url):
        pass
    print driverPay.current_url
    while True:
        time.sleep(0.5)
        driverPay.refresh()
        money = driverPay.find_element_by_xpath(
            '//*[@id="J-assets-balance"]/div[1]/div/div[2]/div/strong').text
        if float(money) > 0.01:
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
serRFID = serial.Serial('Com11', baudrate=115200)
# port = "/dev/ttyUSB2"

goods = set()
print u'串口打开'
while 1:
    line = serRFID.readline().strip()
    if (line[0], line[-1]) == ('A', '1'):
        set.add(1)

    if (line[0], line[-1]) == ('L', '1'):
        set.remove(1)

    if (line[0], line[-1]) == ('A', '2'):
        set.add(2)

    if (line[0], line[-1]) == ('L', '2'):
        set.remove(2)


    l = ''
    for x in goods:
        l = l+str(x)

    if l == '':
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart.html')

    if l == '1':
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart1.html')

    if l == '2':
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart2.html')

    if l == '12':
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart12.html')

    if l == '21':
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart21.html')
    '''
    if (line[0], line[-1]) == ('A', '1'):
        set.add(1)
        print u'接收到1号商品'
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart1.html')

    if (line[0], line[-1]) == ('A', '2'):
        print u'接收到2号商品'
        driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart2.html')
        break
    '''
    if driverShop.current_url.find('pay') != -1:
        break



while flagPay is False:
    pass

urlSuccess = 'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/success.html'
driverShop.get(urlSuccess)
