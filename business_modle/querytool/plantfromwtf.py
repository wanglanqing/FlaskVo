# !flask/bin/env python
# coding:utf-8

from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField, BooleanField, RadioField,DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange,Regexp
from FlaskVv.config import sub_systems,sqls
from FlaskVv.business_modle.VersionTracker.VersionTracker import VersionTracker


class MyForm(Form):
    adzoneClickid = StringField('adzoneClickid', validators=[Length(min=4, max=25)])


class TestCaseForm(Form):
    # 从config配置文件里，读取子系统，构建页面上的group信息
    sss = sub_systems.values()
    ssl = []
    for sub_system in sss:
        ssl.append((sub_system, sub_system))

    # 定义表单元素
    apiName = StringField(validators=[DataRequired()], render_kw={'placeholder': u'广告计划-列表'})
    apiState = RadioField(u'apiState', validators=[DataRequired()], choices=[('1', u'已编写'), ('0', u'未编写')], default='1')
    testCaseName = StringField(u'testCaseName', validators=[DataRequired()], render_kw={'placholder': 'order/list'})
    # status = SelectField(u'status',choices=[('有效','1'),('无效','0')])
    # group=RadioField('group',validators=[],choices=[('yiiqfa','yiiqfa'),('egou','egou'),('hudongtui','hudongtui')])
    group = RadioField('group', validators=[], choices=ssl)
    status = RadioField(label=u'status', validators=[DataRequired()], choices=[('1', u'启用'), ('0', u'停用')], default='1')
    level = IntegerField(u'level', validators=[], render_kw={'placeholder': u'等级1 2 3'})
    param_type = SelectField(u'param_type', choices=[('A', u'错误信息'), ('B', u'数据结构'), ('C', u'状态码')])
    methodurl = TextAreaField(u'methodurl', validators=[DataRequired()],
                              render_kw={'placeholder': 'http://api.demand.adhudong.com/api/voyager/order/list.htm',
                                         'style': 'height:50px', 'style': 'weight:200px'})
    param = TextAreaField(u'param', validators=[DataRequired()],
                          render_kw={'placeholder': "{'aid':'0'}", 'style': 'height:100px；weight:50px'})
    actresult = IntegerField(u'actresult', render_kw={'placeholder': u'http状态码 e.g 200 302'})
    expect_value = StringField('expect_value')
    remarks = StringField('remarks')
    submit = SubmitField(u'提交保存')


class VersionTrackerForm(Form):
    # 从config配置文件里，读取group，和对应的jobs
    vt = VersionTracker()
    group_choices = list(vt.get_group_info(sqls['group']))
    job_name_choices = list(vt.get_jenkins_job(sqls['jenkins_job']))
    applicant_choices = list(vt.get_user_info(sqls['applicant']))
    tester_choices = list(vt.get_user_info(sqls['tester']))
    approver_choices = list(vt.get_user_info(sqls['approver']))

    group = RadioField(u'group', validators=[DataRequired()], choices=group_choices, default=1)
    job_name = SelectField(u'job_name', choices=job_name_choices) #通过group级联选择？
    applicant = SelectField(u'applicant', validators=[DataRequired()], render_kw={'placeholder': u'开发者姓名'}, choices=applicant_choices)  # 是否需要配置
    approver = SelectField(u'approver', render_kw={'placeholder': u'审批人姓名'}, choices=approver_choices)  # 是否需要配置
    ol_type = StringField(u'ol_type', render_kw={'placeholder': u'上线类型'})  #默认为当天时间
    apply_date = StringField(u'apply_date',validators=[DataRequired()], default=vt.get_date()) #默认为当天时间
    ol_date = StringField(u'ol_date',validators=[DataRequired()], default=vt.get_date()) #, validators=[DataRequired()]
    version = StringField(u'version', validators=[DataRequired(message=u'请输入版本号'), Regexp('[0-9]')], render_kw={'placeholder': u'项目版本号信息','pattern':'[0-9A-Za-z]*'})  # 是否需要配置,Regexp()
    v_tag = StringField(u'tag', render_kw={'placeholder': u'项目版本tag信息','style':' width="30px"'})  # 是否需要配置
    v_desc = TextAreaField(u'v_desc',render_kw={'placeholder':u'上线内容描述'})
    tester = SelectField(u'tester', render_kw={'placeholder': u'测试人姓名'}, choices=tester_choices)  # 是否需要配置
    remark = TextAreaField(u'remark', render_kw={'placeholder': u'备注信息'})
    send_email = RadioField(u'是否发送邮件通知sys', choices=[('1', u'是'), ('0', u'否')],default=0)
    submit = SubmitField(u'提交保存')