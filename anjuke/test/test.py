# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from anjuke.items import *


if __name__ == '__main__':
    print (re.match("(.*)年","1200年").group(1))

    print(re.match("(.*)\(", "中层(共9层)").group(1))

    target = "\n\t\t555.1万     "
    target = target.strip()
    result = re.match("(.*)万", target).group(1)
    print (int(float(result)*10000))

    result = re.match(".*view/(.*)\?.*","https://guangzhou.anjuke.com/prop/view/A1276635348?from=filter&spread=commsearch_p&position=1&kwtype=filter&now_time=1529218783")
    print (result.group(1))


    ttt = u'\uff0d\n\t\t\t\t\t\t\t\u524d\u8fdb\u8def80\u53f7'
    # sss = re.match(".*([\u4e00-\u9fa5]+)",ttt)
    sss = re.match("524d",ttt)
    print (sss)


    ttt = "\n\t\t\t\t\t5室\n\t\t\t\t\t2厅\n\t\t\t\t\t4卫\n\t\t\t\t"
    sss = ''.join(ttt.split())
    print (sss)


    ttt = "低层(共18层)\t\t\t\t"
    sss = re.match("(.*)\(", ttt).group(1)
    print (sss)


    # unicode 编码
