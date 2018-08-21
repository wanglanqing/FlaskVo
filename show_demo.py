# coding:utf8
from flask import Flask,jsonify,request,render_template,url_for
import traceback
from get_act import *
from create_template import *
from myException import *
from confparas import *
from get_act import *
from FlaskVv.business_modle.querytool.plantfromwtf import *
from FlaskVv.hdt_tools.utils.db_info import *
from hdt_tools.utils.db_info import *
# from business_modle.querytool import bidding_analysis as ba
from FlaskVv.business_modle.apitool.apiTool import *
from FlaskVv.business_modle.VersionTracker.VersionTracker import VersionTracker
from flask_mail import Message,Mail
from FlaskVv.utils.Emar_SendMail_Attachments import *
from FlaskVv.config import mail_template,sqls
from business_modle.launch import launchlistdb as lc
from business_modle.querytool import plantfromwtf as ft

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
app = Flask(__name__)
app.config.from_object('config')
app.config['MAIL_DEBUG'] = True
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_SERVER'] = 'smtp.emar.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USERNAME'] = 'wanglanqing@emar.com'
app.config['MAIL_PASSWORD'] = ''
mail = Mail(app)
global env_dict
env_dict={u'测试环境':True,u'生产环境':False}
@app.route('/')
def index():
    print 'ok'
    return render_template("index.html")


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
            print(temlate_name_re)
            if temlate_name_re.json()['code'] == 200:
                temlate_name_fe = '创建模板【' + temlate_name + '】,成功了，返回结果是: \n' + temlate_name_re.text
            else:
                # raise myException('create_template ', temlate_name_re.text)
                raise myException('create_template ', temlate_name_re)

            # # 创建活动，create_act(self, act_name,free_num=20, award_num=6)
            act_re = ct.create_act(free_num)
            print(act_re)
            if act_re.json()['code'] == 200:
                act_fe = '创建活动【' + act_name + '】,成功了，返回结果是: \n' + act_re.text
            else:
                raise myException('create_act ', act_re.text)

            # # 创建活动关联的奖品，
            awards_re = ct.create_awards()
            print(awards_re)
            # return render_template("create_act.html",  act_re=template_type_fe, awards_re =awards_re )

            ##关联广告位
            adzone_re = ct.adzone_act()
            return render_template("create_act.html", template_type_re=template_type_fe, temlate_name_re=temlate_name_fe , act_re=act_fe, awards_re =awards_re ,adzone_re=adzone_re)
        except Exception as e:
            traceback.print_exc()
            return render_template("create_act.html", f_re = e.message)

@app.route('/jssdk/')
def jssdk():
    return render_template('jssdk.html')

@app.route('/confparas/', methods=['POST','GET'])
def confparas():
    title = u'数据库配置表'
    if request.method=='GET':
        return render_template("confparas.html",title = title)
    else:
        env = request.form.get('env').strip()
        print(env)
        # env_dict={'测试环境':True,'生产环境':False}
        env_dict={u'测试环境':True, u'生产环境':False}
        print(env_dict[env])
        paras = ConfParas(env_value=env_dict[env]).manager_paras()
        return render_template('confparas.html', title = title, paras = paras,env = env)

@app.route('/ad_simulation/',methods=['post','get'])
def ad_simulation():
    #如果需要增加查询字段，分别在ad_simulation.html中增加显示该字段，在get_act.py中chk_dict增加映射关系
    title ='模拟投放接口查询'
    if request.method == 'GET':
        return render_template("ad_simulation.html", title=title)
    else:
        env_dict={u'测试环境':'T', u'生产环境':'P'}
        env = request.form.get('env').strip()
        adzoneID = request.form.get('adzoneID')
        adOrderID = request.form.get('adOrderId')
        chklist = request.form.getlist('chklist')
        if adzoneID and chklist:
            final = get_ad_simulation_info(adzoneID, adOrderID, chklist, env_value=env_dict[env])
            print('===========',final)
            #chklist返回的为表头，final_k返回的为[[id,id,id],[id,id]] ，final_len返回的有多少个广告
            if isinstance(final,dict):
            # if adzoneID in final:
                chklist.insert(0, u'序号')
                return render_template("ad_simulation.html", title=title, chklist=chklist ,final_k=final.values(),final_len=range(len(final)))
            else:
                print( u'序号')
                return render_template("ad_simulation.html", title=title, emsg=final, knowledge=knowlegde())
        else:
            return render_template("ad_simulation.html", title=title,emsg='请输入广告位id或勾选关键字')

@app.route('/AAS/',methods=['post', 'get'])
# @app.route('/ad_simulation/',methods=['post','get'])
def act_template():
    title = '通过模板查询活动'

    #获取前台传入的参数
    newframe = request.form.getlist('newframe')
    oldframe = request.form.getlist('oldframe')
    env = request.form.get('env')

    # return render_template("act_template.html", title=title, newframe=newframe, oldframe=oldframe)
    return render_template("act_template.html")

# @app.route('/apiTestCase/', methods=('POST','GET'))
@app.route('/Api_index/testCase/', methods=('POST','GET'))
def TestCase():
    form = TestCaseForm()
    at = Api()
    if form.is_submitted():
        sql_data = form.data
        sql_data.pop('csrf_token')
        sql_data.pop('submit')
        keys = tuple(sql_data.keys())
        values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
        re=at.insert_case(values_list,keys)
        # sql = r"INSERT INTO test.testcase_adv {} VALUES ".format(keys).replace("'","`")
        # sql = sql + "("  + values_list[1:-1] +")"
        # print sql
        # db.execute_sql(sql)
        # db.mycommit()
        if re != 0:
            print 'sussssssss'
            msg = '添加成功'
        else:
            print 'failllllllllll'
            msg = '添加失败'
        return render_template('testCase.html',  form = form, msg=msg)
    return render_template('testCase.html', form = form)


@app.route('/Api_index/')
def api_index():
    at = Api()
    re = at.query_api_stat_summary()
    return render_template('apiStatic.html',re =re, col_len = len(re[0]))

@app.route('/Api_index/<sub_system>/')
def sub_system(sub_system):
    print sub_system
    title = sub_system
    at = Api()
    static_data = at.query_api_stat_detail(sub_system)
    return render_template('sub_system_static.html',title = title, static_data = static_data, static_count = len(static_data) )

@app.route('/version_maintain/',methods=('POST','GET'))
def version_maintain():
    # mail = Mail(app)
    form = VersionTrackerForm()
    vt = VersionTracker()
    if form.is_submitted():
        sql_data = form.data
        print sql_data
        sql_data.pop('csrf_token')
        sql_data.pop('submit')
        #处理多个tester_id的情况
        tester = json.dumps(sql_data['tester'], encoding='utf-8', ensure_ascii=False)[1:-1].replace("\"", "")
        #使用update将字典tester的值为ids，如2,4,3
        sql_data.update(tester=tester)
        # tester_name = json.dumps(vt.get_user_ch_name(sqls['ch_name'].format(tester_ids)), encoding='utf-8', ensure_ascii=False)
        keys = tuple(sql_data.keys())
        values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
        re = vt.insert_version(values_list, keys)
        if re != 0:
            msg = '添加成功'
            if form.data['send_email'] != 0:
                #拼装邮件内容申请者姓名、审批者姓名和邮件发送者的拼音、jobname信息
                applicant = vt.get_user_ch_name(sqls['ch_name'].format(form.data['applicant_id']))[0][0]
                approver = vt.get_user_ch_name(sqls['ch_name'].format(form.data['approver']))[0][0]
                sender = vt.get_user_ch_name(sqls['ch_name'].format(tester))[0][1]
                job_name = vt.get_jenkins_job(sqls['jenkins_job'].format(form.data['job_id']))[0][1]
                print job_name
                send_email(mail_template['normal'], form.data, applicant, approver,sender,job_name)
        else:
            msg = '添加失败'

        return render_template('VersionTracker/version_maintain.html', form=form, msg=msg)
    # msg = Message(subject='test send mail', sender='wanglanqing@emar.com', recipients=['wanglanqing@emar.com'])
    # msg.body = 'send by testr'
    # msg.html = '<p>中文对么？</p>'
    # print '****************************'
    # mail.send(msg)

    return render_template('VersionTracker/version_maintain.html',form = form)

@app.route('/launchlist/',methods=['GET','POST'])
def launchlist():
    form=ft.Mylaunchlist()
    x=form.myyear
    if form.is_submitted():
        year=form.myyear.data
        month=form.mymonth.data
        #增加两个字段
        group_id = form.groups.data
        tester_id = form.testers.data
        print month,year
        reslut=lc.getlanuchlist(int(year),int(month),int(group_id),int(tester_id))
        if len(reslut)>0:
            lc.exportXls(reslut)
        return render_template('launchlist.html',form=form,result=reslut)
    else:
        return render_template('launchlist.html',form=form,result='')

# @app.route('/export/',methods=['post','get'])
# def exportXls():


if __name__ == '__main__':
    # app.configs['JSON_AS_ASCII'] = False
    app.run( host="0.0.0.0", port=9000, debug=True)


