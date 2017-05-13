#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-19 14:40:53
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$


import socket

# 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
follow = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
follow.bind(('0.0.0.0', 5555))  # 绑定本机IP和任意端口(>1024)
print u'the server of follow is running'
followSock, addr = follow.accept()  # 接收一个新连接
print 'the client of follow has connected'
followSock.send('start'.encode())

