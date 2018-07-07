# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from urllib import parse
from scrapy.loader import ItemLoader
from anjuke.items import *
import re
import logging
from anjuke.utils.LoggerUtil import LogUtils

loggerDataName = "anjuke"
log_dataInfo_path = "logs/anjuke.log"
log = LogUtils.createLogger(loggerDataName, log_dataInfo_path)


class AnjukeGzSpider(scrapy.Spider):

    name = 'anjuke_gz'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://guangzhou.anjuke.com/sale/']

    headers = {
        "HOST": "guangzhou.anjuke.com",
        "Referer": "https://guangzhou.anjuke.com",
        'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0"
    }

    def parse(self, response):
        items = response.css("#houselist-mod-new > li")
        log.info("正在处理_list:%s,条数:%s" %( response.url ,len(items)))

        # 获取列表
        for itemnode in items:

            itemurl = itemnode.css('a.houseListTitle::attr(href)').extract()
            itemtitle = itemnode.css('a.houseListTitle::attr(title)').extract()
            log.info("list中显示:%s,标题:%s" % (itemurl, itemtitle))

            # print('%s,链接为:%s' % (itemtitle[0], itemurl[0]))
            yield Request(url=parse.urljoin(response.url, itemurl[0]), meta={"refer_url": response.url},
                          callback=self.parse_detail, headers=self.headers)

        # 获取下一页
        nexturlArr = response.css('#content > div.sale-left > div.multi-page > a.aNxt::attr(href)').extract()
        if nexturlArr:
            nexturl = nexturlArr[0]
            yield Request(url=parse.urljoin(response.url, nexturl), callback=self.parse, headers=self.headers)

    def parse_detail(self, response):
        # "https://guangzhou.anjuke.com/prop/view/A1285389340?from=filter&spread=commsearch_p&position=361&kwtype=filter&now_time=1529215280"
        refer_url = response.meta.get("refer_url", '')
        log.info("正在处理_detail:%s,refer_url为：%s" %( response.url,refer_url))


        match_re = re.match(".*view/(.*)\?.*", response.url)
        id = match_re.group(1)

        citemloader = OrderItemLoader(item=OrderItem(), response=response)
        citemloader.add_value("id", id)
        citemloader.add_css("title", "#content > div.clearfix.title-guarantee > h3::text")
        citemloader.add_css("community_id",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(1) > dd > a::attr(href)")
        citemloader.add_css("community_name",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(1) > dd > a::text")
        citemloader.add_css("area1",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(2) > dd > p > a:nth-child(1)::text")
        citemloader.add_css("area2",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(2) > dd > p > a:nth-child(2)::text")
        citemloader.add_css("build_time",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(3) > dd::text")
        citemloader.add_css("address",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(2) > dd > p::text")
        citemloader.add_css("housetype",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.first-col.detail-col > dl:nth-child(4) > dd::text")
        citemloader.add_css("housestructure",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.second-col.detail-col > dl:nth-child(1) > dd::text")
        citemloader.add_css("space",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.second-col.detail-col > dl:nth-child(2) > dd::text")
        citemloader.add_css("building_floors",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.second-col.detail-col > dl:nth-child(4) > dd::text")
        citemloader.add_css("house_floor",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.second-col.detail-col > dl:nth-child(4) > dd::text")
        citemloader.add_css("direction_face",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.second-col.detail-col > dl:nth-child(3) > dd::text")
        citemloader.add_css("unit_price",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.third-col.detail-col > dl:nth-child(1) > dd::text")
        citemloader.add_css("consult_first_pay",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.third-col.detail-col > dl:nth-child(2) > dd::text")
        citemloader.add_css("decoration_degree",
                            "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-wrap > div > div.third-col.detail-col > dl:nth-child(4) > dd::text")
        # citemloader.add_css("hosedesc", "#content > div.wrapper > div.wrapper-lf.clearfix > div.houseInfoBox > div > div.houseInfo-desc")

        import datetime
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        citemloader.add_value("refer_url", refer_url)
        citemloader.add_value("now_time", nowTime)

        item = citemloader.load_item()
        yield item
        pass
