# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 15:13
# @Author  : wanglanqing


from flask import Blueprint,flash,request,render_template
from .jobAdReason.jobAdReasonForm import JobAdReasonForm
from .jobAdReason.jobAdReason import JobAdReason


#创建蓝图
tools = Blueprint('tools',
                  __name__,
                  template_folder='template'
                  )

@tools.route('/aaa/<any(new,query,excute):page_name>',methods=['POST','GET'])
def aaa(page_name):
    form = JobAdReasonForm()
    jar = JobAdReason()
    if request.method == 'POST' and page_name == 'new':
        form_datas = form.data
        form_datas.pop('csrf_token')
        jar.add_job_ad_reason(form_datas)
        re = jar.get_job_ad_reason_list()
        return render_template('jobAdReason.html', form=form, re=re, re_len=range(len(re)))
    elif request.method == 'POST' and page_name == 'query':
        id = request.args.get('id')
        jar.add_adzone_click_ids(id)
        re = jar.get_job_ad_reason_list()
        return render_template('jobAdReason.html', form=form, re=re, re_len=range(len(re)))
    else:
        re = jar.get_job_ad_reason_list()
        return render_template('jobAdReason.html', form=form,re=re, re_len=range(len(re)))