#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-03-18 16:53:26
# @Author  : CarryHJR
# @Link    : https://github.com/CarryHJR
# @Version : $Id$

# 导入socket库:
import socket
# 创建一个socket:
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 建立连接:
s.connect(('www.sina.com.cn', 80))
s.send('')
s.close()
