# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 11:40
# @Author  : wanglanqing


import json
from hdt_tools.utils.db_info import *
from utils.ToBeJson import ToBeJson


class JobAdReason(object):
    def __init__(self):
        self.db = DbOperations()
        self.pdb = DbOperations(env_value=True)
        self.jid = 0
        self.jobsql = ""

    def get_job_ad_reason_list(self):
        keys=['id','jobname','ad_order','jobsql','have_adzone_click_ids']
        # ,if(LENGTH(result)>0,'是','否 ,'have_result'
        list_sql = '''select id,jobname,ad_order,jobsql,if(LENGTH(adzone_click_ids)>0,'是','否')
                  from test.job_ad_reason order by id desc; '''
        re = self.db.execute_sql(list_sql)
        return ToBeJson.trans(keys,re)

   #提交sql的表单数据入库
    def add_job_ad_reason(self,form_datas):
        keys = str(form_datas.keys())[1:-1].replace("'", "`")
        values = json.dumps(form_datas.values(), encoding='utf-8', ensure_ascii=False)[1:-1]
        sql = 'insert into test.job_ad_reason ({})  values ({})'.format(keys,values)
        self.db.execute_sql(sql)
        self.db.mycommit()
        self.jid = int(self.db.execute_sql('SELECT @@IDENTITY;')[0][0])
        self.jobsql = form_datas['jobsql']
        self.add_adzone_click_ids()


    #通过传入的sql，查询该广告位的adzone_click_id
    def add_adzone_click_ids(self,id):
        jobsql = self.db.execute_sql("select jobsql from test.job_ad_reason where id ={} ".format(id))
        re = self.db.execute_sql(str(jobsql[0][0]))
        print re
        if re:
            adzone_click_ids = JobAdReason.merge_adzone_click_ids(re)
            update_sql = """UPDATE test.`job_ad_reason` SET `adzone_click_ids`="{}" ,update_time=now() WHERE `id`='{}' """.format(
                adzone_click_ids, id)
        else:
            adzone_click_ids_remark='没有该广告位点击'
            update_sql = "UPDATE test.`job_ad_reason` SET `adzone_click_ids_remark`='{}' ,update_time=now()  WHERE `id`='{}' ".format(adzone_click_ids_remark, id)
        self.db.execute_sql(update_sql)

    @staticmethod
    def merge_adzone_click_ids(re):
        '''
        :param re: 序列类型
        :return:返回用;拼接的字符串
        '''
        ids = ''
        for item in re:
            ids = ids + item[0] + ';'
        return ids[:-1]


if __name__=='__main__':
    pass