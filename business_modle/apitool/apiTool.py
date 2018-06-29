# -*- coding: utf-8 -*-
# @Time    : 2018/6/24 16:22
# @Author  : wanglanqing


from FlaskVv.hdt_tools.utils.db_info import *


class Api(object):
    def __init__(self):
        self.db = DbOperations()
        pass

    def insert_case(self):
        pass

    def update_case(self):
        pass

    def delete_case(self):
        pass

    def query_case(self):
        pass

    def query_api_stat_detail(self, sub_system):
        print sub_system
        sql = r'''select `group`,`actresult`,apiname,count(*) from test.testcase_adv a where a.`group`='{}'  group by  a.apiname,a.actresult;'''.format(sub_system)
        re = self.db.execute_sql(sql)
        return re
        pass

    def query_api_stat_summary(self,sub_system):
        sql =r"select count(*) from test.testcase_adv a where `group`='{}' and apiState=1;".format(sub_system)
        re = self.db.execute_sql(sql)
        return re

    def __del__(self):
        pass