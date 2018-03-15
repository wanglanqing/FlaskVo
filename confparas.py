# -*- coding: utf-8 -*-
# @Time    : 2018/3/14 16:20
# @Author  : wanglanqing

import json
from utils.db_info import *

def query_paras():
    db = DbOperations()
    q_sql = "select type, `desc`,`value`,value_type from voyager.config_parameters where status='1'"
    conf_re = db.execute_sql(q_sql)
    db.close_db()
    conf_all_len = len(conf_re)
    final_re = []
    #取行信息进行处理
    for i in range(conf_all_len):
        row = []
        conf_col_len = len(conf_re[i])
        #取列信息进行处理
        #特殊处理type=13这一行的数据，将value转换为a>b>c的样式
        if conf_re[i][0] == 13:
            type13_row = list(conf_re[i])
            #取出type=13的value值，将unicode转换为str，通过split转换为list
            value_list = type13_row[2].encode("utf-8").split(',')
            type13_row.pop(2)
            value_dict ={}
            #将list转换为字典
            for tmp_value in value_list:
                value_dict[tmp_value[-1]]=tmp_value[:-2]
            #字典按值倒序排序
            value_list = sorted(value_dict.keys(), key=lambda e: e[0], reverse=True)
            #将value转换为a>b>c的样式
            fstr = ''
            for item in value_list:
                fstr += str(value_dict[item]) + ' > '
            type13_row.insert(2, fstr[:-2])
            #重新写入row()
            for fitem in type13_row:
                row.append(fitem)
            print(row)
        else:
            for m in range(conf_col_len):
                row.append(conf_re[i][m])
        final_re.append(row)
    return (final_re)

if __name__ == '__main__':
    query_paras()