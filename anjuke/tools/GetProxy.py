# -*- coding: utf-8 -*-
__author__ = 'bobby'
import requests
from scrapy.selector import Selector
from anjuke.tools.DRedis import DRedis
import random,json
from anjuke.utils.LoggerUtil import LogUtils
from anjuke.settings import *


#redis操作类
redisObj = DRedis()

loggerDataName = "proxy_oper"
log_dataInfo_path = BASE_DIR+"/proxy_oper.log"
log = LogUtils.createLogger(loggerDataName, log_dataInfo_path)

# 参考:https://coding.imooc.com/lesson/92.html#mid=3135

#
# def crawl_ips():
#     #爬取西刺的免费ip代理
#     headers = {"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0"}
#     for i in range(1568):
#         re = requests.get("http://www.xicidaili.com/nn/{0}".format(i), headers=headers)
#
#         selector = Selector(text=re.text)
#         all_trs = selector.css("#ip_list tr")
#
#
#         ip_list = []
#         for tr in all_trs[1:]:
#             speed_str = tr.css(".bar::attr(title)").extract()[0]
#             if speed_str:
#                 speed = float(speed_str.split("秒")[0])
#             all_texts = tr.css("td::text").extract()
#
#             ip = all_texts[0]
#             port = all_texts[1]
#             proxy_type = all_texts[5]
#
#             ip_list.append((ip, port, proxy_type, speed))
#
#         for ip_info in ip_list:
#             cursor.execute(
#                 "insert proxy_ip(ip, port, speed, proxy_type) VALUES('{0}', '{1}', {2}, 'HTTP')".format(
#                     ip_info[0], ip_info[1], ip_info[3]
#                 )
#             )
#
#             conn.commit()

class GetProxy(object):
    def save_ip(self,ip):
        # 保存ip
        prefix = redisObj.getPrefix()
        redisObj.getRedisObj().set(prefix+ip,ip)

    def delete_ip(self, ip):
        #从redid中删除无效的ip
        prefix = redisObj.getPrefix()
        result = redisObj.getRedisObj().delete(prefix+ip)
        print(result)


    def getIPFromSesame(self):
        # 返回列表 ip:port,ip:port形式
        log.info("getIPFromSesame")
        # //这个url在
        sesameurl = SESAME_URL;
        try:
            cresponse = requests.get(sesameurl)
        except Exception as ex:
            log.error("请求芝麻接口失败,错误为:" + ex)
            # 这里要发下邮件 TODO
            return
        #从芝麻中拿到ips的列表

        try:
            resultObj = json.loads(cresponse.content)
        except:
            log.error("解析内容出错,内容为:" + cresponse.content)
            return
        # {"code": 0, "success": true, "msg": "0",
        #  "data": [{"ip": "182.42.156.201", "port": 6856, "expire_time": "2018-07-03 12:22:08", "city": "山东省日照市"},
        #           {"ip": "122.6.92.251", "port": 56856, "expire_time": "2018-07-03 12:22:11", "city": "山东省日照市"},
        #           {"ip": "182.37.101.93", "port": 56856, "expire_time": "2018-07-03 12:22:04", "city": "山东省日照市"}]}
        # code0为成功，1为失败
        # success,true为成功，false为失败markiPport端口city城市（地级市名称）isp运营商（电信、联通）expire_time 过期时间

        code = resultObj.get('code')
        if code!=0:
            errMsg = resultObj.get('msg')
            # 这里应该去发发邮件
            log.error("请求芝麻接口返回code不为0,错误为:"+errMsg)
            # 处理相应的错误日志
            return

        # 拼装相关内容
        ipPortArr = []
        datalist = resultObj.get('data')
        for dataobj in datalist:
            ip = dataobj.get('ip')
            port = dataobj.get('port')
            ipPortArr.append(ip+":"+str(port))

        return ipPortArr

    def operIpPool(self):
        log.info("operIpPool,从远端获取代理数据并扔到redis")
        # 判断下池里有多少数据，如果太多了，就不处理了
        prefix = redisObj.getPrefix()
        proxy_keys_list = redisObj.getRedisObj().keys(prefix+"*")
        if proxy_keys_list and len(proxy_keys_list)>100:
            log.error("redis中的ip已经很多了，不要再请求了!")
            return
        iplist = self.getIPFromSesame()
        if iplist:
            for ip in iplist:
                # ip 是xxx.xxx.xx.xx:xxxx的形式
                self.save_ip(ip)
        else:
            # 返回的ip列表为空,入redis的ip池 不成功

            pass

    def judge_ip(self, ip, port):
        log.info("判断ip是否可用")
        http_url = "http://www.baidu.com"
        proxy_url = "http://{0}:{1}".format(ip, port)
        try:
            proxy_dict = {
                "http":proxy_url,
            }
            response = requests.get(http_url, proxies=proxy_dict)
        except Exception as e:
            log.error("不可用，删除"+ip)
            self.delete_ip(ip)
            return False
        else:
            code = response.status_code
            if code >= 200 and code < 300:
                print ("effective ip")
                return True
            else:
                log.error("返回不成功,不可用，删除" + ip)
                self.delete_ip(ip)
                return False


    def get_random_ip(self):
        # ,参考: https://blog.csdn.net/warrah/article/details/73484825
        log.info("从redis中随机获取一个可用的ip， 里面有judge等判断!")
        prefix = redisObj.getPrefix()
        proxy_keys_list = redisObj.getRedisObj().keys(prefix+"*")

        # TODO,这里判断下list看的元素个数后，重新operIpPool

        if proxy_keys_list:
            if len(proxy_keys_list)!=1:
                index_list = range(1, len(proxy_keys_list))
                key = proxy_keys_list[random.choice(index_list)]
            else:
                key = proxy_keys_list[0]

            targetipAndport =  redisObj.getRedisObj().get(key)
            if targetipAndport:
                try:
                    arr = targetipAndport.split(":")
                    ip = arr[0]
                    port = arr[1]
                    # 判断是否可用
                    if self.judge_ip(ip,port):
                        #ip可用，直接返回
                        log.info(targetipAndport + "judge可用，直接返回")
                        return targetipAndport
                    else:
                        log.info(targetipAndport + "judge不可用，删除并重新获取")
                        self.delete_ip(targetipAndport)
                        self.get_random_ip()
                except Exception as ex :
                    print(ex)
                    log.error(targetipAndport+"的解析出错了，嗯，是入redis的时候错了吗?删除并重新获取ip")
                    self.delete_ip(targetipAndport)
                    self.get_random_ip()
            else:
                log.error( "在redis中获取的key:"+key+",其值为空，删除并重新获取")
                self.delete_ip(targetipAndport)
                self.get_random_ip()
        else:
            log.info("redis中没有数据，从代理服务器中拿列表并存到redis中")
            self.operIpPool()
            return self.get_random_ip()


# print (crawl_ips())
if __name__ == "__main__":
    gproxy = GetProxy()
    # gproxy.getIPFromSesame()
    # gproxy.operIpPool()
    currentip = gproxy.get_random_ip()
    log.info("得到的ip为:"+str(currentip))

    # targetipAndport = "1212.12.12.12:80"
    # arr = targetipAndport.split(":")
    # log.info(arr)