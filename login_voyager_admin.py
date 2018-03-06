# -*- coding: utf-8 -*-
# @Time    : 2018/2/24 14:56
# @Author  : wanglanqing

import requests

def login_voyager_admin():
    s = requests.session()
    s.get('http://api.admin.adhudong.com/login/login_in.htm?name=test&pwd=qq')
