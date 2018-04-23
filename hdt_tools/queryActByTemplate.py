# -*- coding: utf-8 -*-
# @Time    : 2018/4/10 9:40
# @Author  : wanglanqing

import paramiko
from utils.db_info import *

class queryActs(object):
    def __init__(self):
        # self.db = DbOperations(env_value=env_value)
        # self.newframe = newframe
        # self.oldframe = oldframe
        self.frame_dict = {'九宫格': 'sharp-lottery',
                 '轮盘': 'rotary-tableTe',
                 '刮刮卡': 'scratch-card',
                 '新轮盘': 'rotary-table',
                 '花生好车': 'peanutCar',
                 '幸运大富翁': 'moneybags',
                 '老虎机': 'lottery_machine',
                 '抓娃娃': 'lottery-claw',
                 '扭蛋': 'Gashapon',
                 '翻牌': 'draw-card',
                 '交行信用卡模板类型': 'creditCard',
                 '套牛': 'steer_roping',
                 '': '', }
        self.host='101.254.242.11'
        self.port= '20002'
        self.username= 'wanglanqing'
        # self.password= '0000001234'
        pass

    def get_template_info(self):
        private_key = paramiko.RSAKey.from_private_key_file(r"C:\Users\liuguanlong\.ssh\id_rsa")
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        # client.set_missing_host_key_policy(paramiko.WarningPolicy)
        # client.connect(self.host, port=self.port, username=self.username, password=self.password, compress=True)
        client.connect(hostname='101.254.242.11', port=20002, username='wanglanqing', pkey=private_key)
        # client.connect(hostname, port, username, password, compress=True)
        stfp_client = client.open_sftp()
        remote_file = stfp_client("/data/voyager/git/display/app/client/routes.js")
        try:
            for line in remote_file:
                print(line)
        finally:
            remote_file.close()

if __name__=='__main__':
    qa = queryActs()
    qa.get_template_info()