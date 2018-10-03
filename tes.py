# -*- coding: utf-8 -*-
# @Time    : 2018/5/22 10:04
# @Author  : wanglanqing
# encoding=utf-8
__author__ = 'aidinghua'
import requests
from hdt_tools.utils.db_info import *
import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField, BooleanField, RadioField,DateField,SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange,Regexp
from FlaskVv.config import sub_systems,sqls
from FlaskVv.business_modle.VersionTracker.VersionTracker import VersionTracker
import datetime


class AD_List (object):
    def __init__(self):
        self.db = DbOperations()
        self.r=requests.session()
        self.r.get('http://api.admin.adhudong.com/login/login_in.htm?name=test&pwd=!Qq123456 ')

    def adlist(self):
        url= 'http://api.admin.adhudong.com/advertiser/list.htm?'
        payload={"page":1,"page_size":200}
        re=self.r.get(url,params=payload)
        return  re.text

    def test_hebing(self):
        tmpsql = '''SELECT g.name 业务组,j.name 项目,u.ch_name 开发 ,ut.ch_name 测试,v.version,v.v_desc,v.create_time from test.version_tracker v
            INNER JOIN  test.group  g on v.group_id=g.id
            INNER JOIN test.jenkins_job j on v.job_id=j.id
            INNER JOIN test.user u on v.applicant_id=u.id
            INNER JOIN test.user ut on v.tester=ut.id
            where g.status=1 and j.status=1 and u.status=1'''
        tmpsql2= "select (select group_concat( b.name ) from test.user b where  instr(a.tester,b.id ) > 0) name FROM test.version_tracker a"
        re1 = self.db.execute_sql(tmpsql)
        re2 = self.db.execute_sql(tmpsql2)
        # print type(re1), type(re2)
        re1_len = len(re1)
        re2_len = len(re2)
        if re1_len == re2_len:
            for i in range(re2_len):
                re1[i].append(re2[i][0])
            print 'final resutl'
            print re1
    def mymonth(self):
        return int(datetime.datetime.now().month)

    def testr(self):
        vt = VersionTracker()
        tester_choices = list(vt.get_user_info(sqls['tester']))
        tester_choices.insert(0,(0,'all'))
        print tester_choices

if __name__=='__main__':
    al = AD_List()
    al.testr()