# coding:utf8
from flask import Flask,jsonify,request,render_template,url_for
from get_act import *
from create_template import *
from myException import *


app = Flask(__name__)

@app.route('/actinfo/',methods=['POST','GET'])
def show_act_results():
    title=u'测试结果展示'
    res_re = {}
    if request.method=='GET':
        print 1111111111
    else:
        # ids = request.form.getlist('adzoneIds')
        # ids = request.args.get('adzoneIds')

        # ids = request.values.get('adzoneIds')
        ids = request.form.get('adzoneIds')
        print(ids.split(','))
        if len(ids) != 0:
            res_re = get_ad_simulation_info(ids.split(','))
    return  render_template("show_re.html",res=res_re, title=title)

@app.route('/create_act/', methods=['POST','GET'])
def create_act():
    if request.method=='GET':
        return render_template("create_act.html", template_adr='1111')
    else:
        template_adr= request.form.get('template_adr')
        css_adr="'" + request.form.get('css_adr') + "'"
        template_type_name=request.form.get('template_type_name')
        temlate_name=request.form.get('temlate_name')
        act_name=request.form.get('act_name')
        award_num =request.form.get('award_num')
        try:
            ct = TemplateActCreation(template_type_name, act_name,award_num)
            # 创建模板类型，create_template_type(self, classifi, locationAdress, preview="https://img0.adhudong.com/template/201802/24/999337a35a1a9169450685cc66560a05.png",prizesNum=6)
            template_type_re = ct.create_template_type(template_adr)
            if template_type_re.json()['code'] == 200:
                template_type_fe = '创建模板类型' + template_type_re.text + '成功了'
            else:
                raise myException(sys._getframe().f_code.co_name, template_type_re.text)

            # 创建模板 ct.create_template(templateName, templateStyleUrl)
            temlate_name_re = ct.create_template(temlate_name, css_adr)
            if temlate_name_re.json()['code'] != 200:
                raise myException(temlate_name_re.text)

            # # 创建活动，create_act(self, act_name,free_num=20, award_num=6)
            act_re = ct.create_act()
            print(act_re)
            if act_re.json()['code'] != 200:
                raise myException(act_re.text)
            else:
                act_re = '活动，创建成功'

            # # 创建活动关联的奖品，
            awards_re = ct.create_awards()
            print(awards_re)
            # return render_template("create_act.html",  act_re=template_type_fe, awards_re =awards_re )
            return render_template("create_act.html", template_type_re=template_type_re, temlate_name_re=temlate_name_re , act_re=act_re, awards_re =awards_re )
        except Exception as e:
            f_re = ''
            return render_template("create_act.html", f_re = e.message)

if __name__ == '__main__':
    app.run( host="0.0.0.0", port=9000, debug=True)