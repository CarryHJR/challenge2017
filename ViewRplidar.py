#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-04-15 15:35:59
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$

import matplotlib.pyplot as plt
import socket
import time
import json
import threading

# 创建socket (AF_INET:IPv4, AF_INET6:IPv6) (SOCK_STREAM:面向流的TCP协议)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('0.0.0.0', 5555))  # 绑定本机IP和任意端口(>1024)
s.listen(4)  # 监听，等待连接的最大数目为1
print('客户端已就绪')


def tcplink(sock, addr):  # TCP服务器端处理逻辑

    print('Accept new connection from %s:%s.' % addr)  # 接受新的连接请求
    while True:
        data = sock.recv(1024)  # 接受其数据
        print data
        try:
            data = json.loads(data)
        except Exception, e:
            print 'loads failed'
        a = []
        b = []
        for x in data:
            a.append(x[1])
            b.append(x[2])
        plt.ion()
        plt.plot(a, b, 'o')
        time.sleep(1)
        # time.sleep(1)  # 延迟
        if not data == 'quit':  # 如果数据为空或者'quit'，则退出
            break
    sock.close()  # 关闭连接
    print('Connection from %s:%s closed.' % addr)

# data = [(1, 134, 234), (2, 145, 224), (5, 278, 332)]
# a = []
# b = []
# for x in data:
#     a.append(x[1])
#     b.append(x[2])
# plt.ion()
# plt.plot(a, b, 'o')
# a = raw_input()
# plt.cla()
# a = raw_input()


while True:
    try:
        sock, addr = s.accept()  # 接收一个新连接
        t = threading.Thread(target=tcplink, args=(sock, addr))
        t.start()
    except Exception, e:
        print e
