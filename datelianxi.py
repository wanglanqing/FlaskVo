# -*- coding: utf-8 -*-
# @Time    : 2018/4/24 9:00
# @Author  : wanglanqing

import datetime
import requests

now = datetime.datetime.now()
# print(now.date())
# print now.strftime('%Y-%m-%d %H:%M:%S')

# datetime.timedelta(days=0, seconds=0, milliseconds=0, microseconds=0, minutes=0, hours=0, weeks=0)

sday ='2018-04-10'
for i in range(3):
    d1=datetime.datetime.strptime(sday, '%Y-%m-%d')
    delta = datetime.timedelta(days=1)
    n_days = d1-delta
    sday =n_days.strftime('%Y-%m-%d')
    url ='http://api.admin.adhudong.com/repeatReportDay.htm?date_str=' + sday
    re = requests.get(url).json()
    print(re)