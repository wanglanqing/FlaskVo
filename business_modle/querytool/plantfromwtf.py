#!flask/bin/env python
#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField,BooleanField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange
from FlaskVv.config import sub_systems

class MyForm(Form):
    adzoneClickid = StringField('adzoneClickid', validators=[Length(min=4, max=25)])


class TestCaseForm(Form):
    #从config配置文件里，读取子系统，构建页面上的group信息
    sss = sub_systems.values()
    ssl =[]
    for sub_system in sss:
        ssl.append((sub_system,sub_system))

    #定义表单元素
    apiName = StringField(u'apiName', validators=[DataRequired()],render_kw={'placeholder':u'广告计划-列表'})
    apiState = RadioField(u'apiState',validators=[DataRequired()],choices=[('1', u'已编写'), ('0', u'未编写')], default = '1')
    testCaseName = StringField(u'testCaseName',validators=[DataRequired()],render_kw={'placholder':'order/list'})
    # status = SelectField(u'status',choices=[('有效','1'),('无效','0')])
    # group=RadioField('group',validators=[],choices=[('yiiqfa','yiiqfa'),('egou','egou'),('hudongtui','hudongtui')])
    group=RadioField('group',validators=[],choices=ssl)
    status = RadioField(label=u'status',validators=[DataRequired()],choices=[('1', u'启用'),('0', u'停用')],default='1')
    level = IntegerField(u'level',validators=[],render_kw={'placeholder':u'等级1 2 3'})
    param_type = SelectField(u'param_type', choices=[('A',u'错误信息'), ('B', u'数据结构'), ('C', u'状态码')])
    methodurl = TextAreaField(u'methodurl', validators=[DataRequired()],render_kw={'placeholder':'http://api.demand.adhudong.com/api/voyager/order/list.htm','style':'height:150px'})
    param = TextAreaField(u'param', validators=[DataRequired()],render_kw={'placeholder':"{'aid':'0'}",'style':'height:50px'})
    actresult = IntegerField(u'actresult',render_kw={'placeholder':u'http状态码 e.g 200 302'})
    expect_value=StringField('expect_value')
    remarks=StringField('remarks')
    submit = SubmitField(u'提交保存')