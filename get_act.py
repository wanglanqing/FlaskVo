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
def get_ad_simulation_info(adzoneId, checkedList):
    '''
    传入广告位的list，如['372','412']
    输出的为每个广告位上要展示的创意、订单及对应的广告主的信息，返回类型为字典
    字典结构为：
    num：
    '''
    bidTime = datetime.datetime.now().strftime('%Y-%m-%d')
    adzoneId = str(adzoneId)

    re_dict={}
    if len(adzoneId)== 0 :
        return ('请输入广告位id')
    else:
        result_dict = {}
        url = "http://101.254.242.11:17091/ad_simulation.do?positionId=1&adZoneId={0}&bidTime={1}".format(adzoneId, bidTime)
        # try:
        response = requests.get(url, cookies=mycookies).json()['data'][adzoneId]
        res_len = len(response)
        for i in range(res_len):
            re = response[i]
            chk_dict = {'adOrderID': re['adOrder']['id'], 'adOrderName': re['adOrder']['name'],
                        'adCreativeID': re['adCreative']['id'], 'adCreativeName': re['adCreative']['name'],
                        'advertiserId': re['adCreative']['advertiserId']}
            tmp_dict = {}
            for chk in checkedList:
                tmp_value = chk_dict[chk]
                tmp_dict[chk] = tmp_value
            result_dict[i]=tmp_dict
        return result_dict
        # return (json.dumps(result_dict, ensure_ascii=False))

if __name__=='__main__':
    #模拟投放接口
    # get_ad_simulation_info(['371', '372'])
    get_ad_simulation_info(372,['adOrderID','adCreativeID'])


