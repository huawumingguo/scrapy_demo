# -*- coding: utf-8 -*-
__author__ = 'dgm'

import redis
import anjuke.settings as setting


r = redis.Redis(host=setting.REDIS_HOST,port=setting.REDIS_PORT,db=setting.REDIS_DB_INDEX,decode_responses=True)

redis_pre = "IPFORPROXY:"

class DRedis(object):
    def getPrefix(self):
        return  redis_pre

    def getRedisObj(self):
        return  r

if __name__ == "__main__":
    dredis = DRedis()
    dredis.getRedisObj().setex(redis_pre+"119.20.11.10:541","119.120.101.10:5411",60*10)

    keys = dredis.getRedisObj().keys(redis_pre+"*")
    for key in keys:
        print(key)