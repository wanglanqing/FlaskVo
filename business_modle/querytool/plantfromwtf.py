#!flask/bin/env python
#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField,BooleanField,RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, NumberRange

class MyForm(Form):
    adzoneClickid = StringField('adzoneClickid', validators=[Length(min=4, max=25)])


class TestCaseForm(Form):
    apiName = StringField(u'apiName', validators=[DataRequired()])
    apiState = RadioField(u'apiState',validators=[DataRequired()],choices=[('1', u'已编写'), ('0', u'未编写')], default = '1')
    testCaseName = StringField(u'testCaseName',validators=[DataRequired()])
    # status = SelectField(u'status',choices=[('有效','1'),('无效','0')])
    group=RadioField('group',validators=[],choices=[('yiiqfa','yiiqfa'),('egou','egou'),('hudongtui','hudongtui')])

    status = RadioField(label=u'status',validators=[DataRequired()],choices=[('1', u'启用'),('0', u'停用')],default='1')
    level = IntegerField(u'level',validators=[])
    param_type = SelectField(u'param_type', choices=[('A',u'错误信息'), ('B', u'数据结构'), ('C', u'状态码')])
    methodurl = TextAreaField(u'methodurl', validators=[DataRequired()])
    param = TextAreaField(u'param', validators=[DataRequired()])
    actresult = IntegerField(u'actresult')
    expect_value=StringField('expect_value')
    remarks=StringField('remarks')
    submit = SubmitField(u'testcase')