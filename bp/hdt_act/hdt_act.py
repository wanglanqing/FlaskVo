# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 9:52
# @Author  : wanglanqing

from flask import Blueprint, request, render_template
from business_modle.relate.adzoneActForm import adzoneActForm
from business_modle.relate.relateAdzoneAds import relateAdzoneAct
#创建活动蓝图
act = Blueprint('act', __name__,template_folder='templates')

#广告位关联活动
@act.route('adzoneAct/',methods=['GET','POST'])
def adzoneAct():
    form = adzoneActForm()
    if request.method == 'GET':
        return render_template('adzoneAct.html',form=form,pos=0)
    else:
        adzoneId = request.form.get('adzoneId').strip()
        acts = request.form.get('acts').strip()
        RAA = relateAdzoneAct(adzoneId,acts)
        RAA.updateAdzoneAct()
        link = RAA.get_link()
        adzone =  RAA.get_adzone_url()
        return render_template('adzoneAct.html', form=form, pos=1, link=link, adzone=adzone)