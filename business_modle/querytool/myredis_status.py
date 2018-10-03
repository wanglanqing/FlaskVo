# encoding=utf-8
__author__ = 'aidinghua'

# from rediscluster import StrictRedisCluster

def mygetredis(redis_nodes):
    # redis_nodes=[{"host":'101.254.242.11',"port":'17001'},{"host":'101.254.242.12',"port":'17001'},{"host":'101.254.242.17',"port":'17001'}]
    r = StrictRedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
    # print r.hgetall('voyager:budget')
    order_status=r.hgetall('voyager:status')
    # print type(mybudget)
    # 负数的订单个数
    j=0
    for i in  order_status:
        if str(order_status[i])[:1]=='-':
            j=j+1
        print '订单为:'+str(i)+' 状态为: '+str(order_status[i])
    return order_status,len(order_status),j
if __name__ == '__main__':
    # redis_nodes=[{"host":'101.254.242.11',"port":'17001'},{"host":'101.254.242.12',"port":'17001'},{"host":'101.254.242.17',"port":'17001'}]
    redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
    tmp,allcount,j=mygetredis(redis_nodes)
    print allcount
    print j
    print '111166666'
