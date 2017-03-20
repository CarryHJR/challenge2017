#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-20 20:33:41
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$

from selenium import webdriver
driverShop = webdriver.Chrome()
driverShop.get(
            'file:///home/carry/workplace/MyPython/challenge/wwwroot2/www.lovingling.com/shopcart2.html')

while 1:
    if driverShop.current_url.find('pay') != -1:
        break
print 'ok'
