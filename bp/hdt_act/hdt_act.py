# -*- coding: utf-8 -*-
# @Time    : 2019/1/28 9:52
# @Author  : wanglanqing

import traceback
from flask import Blueprint, request, render_template
from business_modle.relate.adzoneActForm import adzoneActForm
from business_modle.relate.relateAdzoneAds import relateAdzoneAct
from business_modle.templateToAct.templateAct import templateAct
from business_modle.templateToAct.templateActForm import templateActForm
from business_modle.checkRoute.checkRouteForm import *
from business_modle.checkRoute.checkRoute import checkNodeRoute
from business_modle.querytool.create_template import *
from business_modle.querytool.myException import *

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

#活动模板互查工具
@act.route('/templateToAct/<any(query,position):page_name>/',methods=['get','post'])
def templateToAct(page_name):
    form=templateActForm()
    if request.method=='GET' and page_name=='query':
        return render_template('template/templateToAct.html', ts='false', form=form)
    elif request.method == 'POST' and page_name == 'query':
        act_ids = request.form.get('ad_ids')
        env = request.form.get('env')
        template_kws = request.form.get('template_kws')
        tta = templateAct(env)
        if template_kws:
            template_kws = template_kws.encode('utf-8')
        re = tta.get_infos(template_kws, act_ids)
        if isinstance(re,list) and len(re)>0:
            tta.exportTemplateXls(re)
            return render_template('template/templateToAct.html', ts='true', form=form,re=re,env=env, flag='true')
        else:
            return render_template('template/templateToAct.html', ts='true', form=form,re=re,env=env, flag='flase')
    elif page_name == 'position' and request.method == 'GET':
        position_id = request.args.get('id')
        env_tmp = request.args.get('env')
        tta2 = templateAct(env_tmp)
        position_re = tta2.get_position(position_id)
        return render_template('template/position.html', re=position_re)

#活动检查路由
@act.route('/checkRoute/',methods=['get','post'])
def checkRoute():
    form = checkRouteForm()
    re = ''
    if request.method == 'GET':
        return render_template('checkRoute.html',form = form,re=re)
    else:
        datas = form.data
        env = datas['env'].strip()
        adzoneLink = datas['adzoneLink'].strip()
        cr = checkNodeRoute(env,adzoneLink)
        re = cr.join_url()
        if isinstance(re,list) and len(re)>0:
            re_len = len(re)
            return render_template('checkRoute.html', form=form, re=re, re_type=1,re_len=re_len)
        else:
            return render_template('checkRoute.html',form = form,re=re,re_type=0)

#创建活动
@act.route('/create_act/', methods=['POST','GET'])
def create_act():
    if request.method=='GET':
        return render_template("create_act.html", template_adr='1111')
    else:
        template_adr= request.form.get('template_adr').strip()
        css_adr =  request.form.get('css_adr').strip()
        template_type_name=request.form.get('template_type_name').strip()
        temlate_name=request.form.get('temlate_name').strip()
        #增加模板配置字段
        template_conf_items= str(request.form.get('template_conf_items')).strip()
        act_name=request.form.get('act_name').strip()
        award_num =int(request.form.get('award_num'))
        free_num = int(request.form.get('free_num').strip())
        request.accept_charsets
        try:
            ct = TemplateActCreation(template_type_name, act_name,award_num)
            # 创建模板类型，create_template_type(self, classifi, locationAdress, preview="https://img0.adhudong.com/template/201802/24/999337a35a1a9169450685cc66560a05.png",prizesNum=6)
            template_type_re = ct.create_template_type(template_adr)
            if template_type_re.json()['code'] == 200:
                template_type_fe = '创建模板类型【' +template_type_name + '】,成功了，返回结果是: \n' + template_type_re.text
            else:
                raise myException('create_template_type ', template_type_re.text)

            # 创建模板 ct.create_template(templateName, templateStyleUrl)
            temlate_name_re = ct.create_template(temlate_name, css_adr, template_conf_items=template_conf_items)
            # print(temlate_name_re)
            if temlate_name_re.json()['code'] == 200:
                temlate_name_fe = '创建模板【' + temlate_name + '】,成功了，返回结果是: \n' + temlate_name_re.text
            else:
                raise myException('create_template ', temlate_name_re)

            # # 创建活动，create_act(self, act_name,free_num=20, award_num=6)
            act_re = ct.create_act(free_num)
            # print(act_re)
            if act_re.json()['code'] == 200:
                act_fe = '创建活动【' + act_name + '】,成功了，返回结果是: \n' + act_re.text
            else:
                raise myException('create_act ', act_re.text)

            # # 创建活动关联的奖品，
            awards_re = ct.create_awards()
            # print(awards_re)
             ##关联广告位
            adzone_re = ct.adzone_act()
            return render_template("create_act.html", template_type_re=template_type_fe, temlate_name_re=temlate_name_fe , act_re=act_fe, awards_re =awards_re ,adzone_re=adzone_re)
        except Exception as e:
            traceback.print_exc()
            return render_template("create_act.html", f_re = e.message)