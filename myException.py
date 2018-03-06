# -*- coding: utf-8 -*-
# @Time    : 2018/3/6 9:06
# @Author  : wanglanqing

class myException(Exception):
    def __init__(self,message):
        Exception.__init__(self)
        self.message=message