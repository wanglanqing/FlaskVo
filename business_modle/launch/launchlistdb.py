#encoding:utf-8
import MySQLdb as mysql ,time,datetime,calendar
from openpyxl import Workbook,worksheet
def myc():
    # db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyager',port=5701,charset='utf8')
    db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='test',port=5701,charset='utf8')
    db.autocommit(True)
    myc=db.cursor()
    return myc,db
def selectsql(sql):
    tmpmyc,tmpdb=myc()
    try:
        tmpmyc.execute(sql)
        result=tmpmyc.fetchall()
    except:
        raise SystemError
    tmpmyc.close()
    tmpdb.close()
    return result
def instertsql(sql):
    tmpmyc,tmpdb=myc()
    try:
        tmpmyc.execute(sql)
        tmpdb.commit()
    except:
        tmpdb.rollback()
        raise SystemExit
    tmpdb.close()
def lanuchlisttmpsql(group,project,src_version,Changes):
    tmpsql='''INSERT INTO `voyagerlog`.`launchlist` ( `group`, `status`, `project`, `src_version`, `Changes`, `createtime`, `updatetime`)
    VALUES ('%s', '1', '%s', '%s', '%s', '%s', '%s');'''%(group,project,src_version,Changes,str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    return tmpsql

def getlanuchlist(year,month,group_id, test_id):
    day_begin = '%d-%02d-01' % (year, month)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(year, month)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d' % (year, month, monthRange)
    # tmpsql='''SELECT `id`, case when `group`= 1 then '互动推' else '其他' end, case when `status`= 1 then '上线成功' else '未知' end , `project`, `src_version`, `Changes`, `createtime`, `updatetime`
    # from voyagerlog.launchlist where createtime>'%s' and createtime<'%s'''%(day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by createtime desc '

    tmpsql='''SELECT g.name 业务组,j.name 项目,u.ch_name 开发 ,ut.ch_name 测试,v.version,v.v_desc,v.create_time from test.version_tracker v
        INNER JOIN  test.group  g on v.group_id=g.id
        INNER JOIN test.jenkins_job j on v.job_id=j.id
        INNER JOIN test.user u on v.applicant_id=u.id
        INNER JOIN test.user ut on v.tester=ut.id
        where g.status=1 and j.status=1 and u.status=1 and '''#g.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
    if test_id == 0:
        tmpsql = tmpsql + '''g.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
        result=selectsql(tmpsql)
    else:
        tmpsql = tmpsql + '''g.id=%s and ut.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,test_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
        result = selectsql(tmpsql)
    return result
def getlanuch(id):
    tmpsql='''SELECT `id`, case when `group`= 1 then '互动推' else '其他' end, case when `status`= 1 then '上线成功' else '未知' end , `project`, `src_version`, `Changes`, `createtime`, `updatetime`
    from voyagerlog.launchlist where id=%s'''%id
    print tmpsql
    result=selectsql(tmpsql)
    return result

def exportXls(result):
    #处理传入的sql查询结果，把表头insert到result[0][0]
    if len(result)>0:
        result = list(result)
        result.insert(0,(u' 业务组',u'项目',u'开发' ,u'测试',u'版本',u'描述', u'上线时间'))
        row = len(result)
        wb = Workbook()
        ws = wb.active
        for r in range(row):
            ws.append(result[r])
        # wb.save('../../static/result/result.xlsx')
        wb.save('./static/result/result.xlsx')



if __name__ == '__main__':
    # tmpsql=lanuchlisttmpsql('bidd','321321fdas','fdasfda')
    #
    # print getlanuch(1)
    # print getlanuchlist(2018, 8)[0][0]
    # print len(getlanuchlist(2018, 1))
    exportXls(getlanuchlist(2018, 8))