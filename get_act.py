# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 10:10
# @Author  : wanglanqing

import requests,datetime
import sys,json
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

mycookies = {'adhd_wdata1':"Mi8vMzk4Ly8yLy8yLy81MDUyOC8vMTUxNTM4MzY1MDQzMi8vOGQzZGQwMWI5NGU1ZThjZjhmMWU2ZjMwZmIwM2VkMGQvLzQ2YTZlMDEzYzA0OQ%3D%3D"}

#模拟投放接口
def get_ad_simulation_info(adid_list):
    '''
    传入广告位的list，如['372','412']
    输出的为每个广告位上要展示的创意、订单及对应的广告主的信息，返回类型为字典
    字典结构为：
    num：
    '''
    bidTime = datetime.datetime.now().strftime('%Y-%m-%d')
    re_dict={}
    for m in range(len(adid_list)):
        ad_dict={}
        creative_dict = {}
        result_dict = {}
        # print(adid_list[i] + "\'s result")
        url = "http://101.254.242.11:17091/ad_simulation.do?positionId=1&adZoneId={0}&bidTime={1}".format(adid_list[m], bidTime)
        try:
            response = requests.get(url, cookies=mycookies).json()['data'][adid_list[m]]
            res_len=len(response)
            for i in range(res_len):
                re = response[i]
                tmp = re['adOrder']['id']
                tmp_adid=re['adCreative']['advertiserId']
                tmp_ac_id = re['adCreative']['id']
                tmp_ac_name= re['adCreative']['name']
                result_dict[i + 1] = {'主:创:订': [tmp_adid,tmp_ac_id,tmp,tmp_ac_name]}
                if i == res_len-1:
                    re_dict[adid_list[m]] = result_dict
        except Exception as e:
            return (e)
    # print(json.dumps(re_dict, ensure_ascii=False))
    return (json.dumps(re_dict, ensure_ascii=False))

if __name__=='__main__':
    #模拟投放接口
    # get_ad_simulation_info(['371', '372'])
    get_ad_simulation_info(['372','371'])


