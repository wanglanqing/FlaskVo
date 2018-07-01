# -*- coding: utf-8 -*-
# @Time    : 2018/6/24 16:22
# @Author  : wanglanqing


from FlaskVv.hdt_tools.utils.db_info import *
from FlaskVv.config .configs import *


class Api(object):
    def __init__(self):
        # print db_config['voyager_test']
        self.db = DbOperations()
        # self.doc_db = DbOperations(env_value=db_config['voyager_online'])
        self.sub_systems = sub_systems
        pass

    def insert_case(self):
        pass

    def update_case(self):
        pass

    def delete_case(self):
        pass

    def query_case(self):
        pass


    def query_api_stat_detail(self,sub_system):

        sql = r'''select `group`,`actresult`,apiname,count(*) from test.testcase_adv a where a.`group`='{}'  group by  a.apiname,a.actresult;'''.format(sub_system)
        re = self.db.execute_sql(sql)
        return re
        pass

    #分别查询两个数据库，获取total和finished的数据
    def query_api_stat_summary(self):
        ss = sub_systems.keys()
        ids = sub_systems.values()
        re = []
        for id, sub_system in sub_systems.items():
            id_sql = r""
            ss_sql =r"select count(*) from test.testcase_adv a where `group`='{}' and apiState=1;".format(sub_system)
            # id_re = self.doc_db(id_sql)[0][0]
            id_re = 123
            ss_re = self.db.execute_sql(ss_sql)[0][0]
            re_tmp=[sub_system, id_re, ss_re, format(float(ss_re)/float(id_re), '.2%')]
            re.append(re_tmp)
        return re

    def __del__(self):
        pass