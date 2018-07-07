# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy, re
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join


class AnjukeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def re_community_id(value):
    match_re = re.match(".*view/(\d+)$", value)
    result = match_re.group(1)
    return result


def re_address(value):
    try:
        result = re.match(".*(\s+)(.*)", value).group(2)
    except Exception as e:
        print(e)
        result = 'aaaa'
    return result


def re_build_time(value):
    return re.match("(.*)年", value).group(1)


def re_space(value):
    return re.match("(.*)平方米", value).group(1)


def re_building_floors(value):
    return re.match(".*共(\d+)层", value).group(1)


def re_house_floor(value):
    # 一般是  高层(共10层) 这样，也有  共5层
    target  =  re.match("(.*)\(", value)
    if target:
        return target.group(1)
    else:
        return value.strip()


def re_unit_price(value):
    return re.match("(.*)元.*", value).group(1)


def get_second(arr):
    if len(arr) > 0:
        if len(arr) > 1:
            return arr[1]
        else:
            return arr[0]
    else:
        return "cccc"


def re_consult_first_pay(value):
    try:
        target = value.strip()
        result = re.match("(.*)万", target).group(1)
    except Exception as e:
        print(e)
        result = 0
    return int(float(result) * 10000)


def re_consult_month_pay(value):
    return re.match("(.*)元.*", value).group(1)

def getval(value):
    return value

def getridof_blank(value):
    if value:
        valstr = value[0]
    target = ''.join(valstr.split())
    return target


class OrderItemLoader(ItemLoader):
    # 自定义itemloader
    default_output_processor = TakeFirst()


class OrderItem(scrapy.Item):
    id = scrapy.Field()
    title = scrapy.Field(
        output_processor=getridof_blank
    )
    community_id = scrapy.Field(
        input_processor=MapCompose(re_community_id),
    )
    community_name = scrapy.Field()
    area1 = scrapy.Field()
    area2 = scrapy.Field()

    address = scrapy.Field(
        input_processor=MapCompose(re_address),
        output_processor=get_second
    )

    build_time = scrapy.Field(
        input_processor=MapCompose(re_build_time),
    )
    housetype = scrapy.Field()
    housestructure = scrapy.Field(
        output_processor=getridof_blank
    )
    space = scrapy.Field(
        input_processor=MapCompose(re_space),
    )

    building_floors = scrapy.Field(
        input_processor=MapCompose(re_building_floors),
    )

    house_floor = scrapy.Field(
        input_processor=MapCompose(re_house_floor)
    )
    direction_face = scrapy.Field()
    unit_price = scrapy.Field(
        input_processor=MapCompose(re_unit_price)
    )
    consult_first_pay = scrapy.Field(
        input_processor=MapCompose(re_consult_first_pay)
    )
    decoration_degree = scrapy.Field()
    hosedesc = scrapy.Field()
    refer_url = scrapy.Field()
    now_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            
            INSERT INTO `anjuke_order_detail` (`id`,`title`, `community_id`, `community_name`, `area1`, `area2`, `build_time`, `address`, `housetype`, `housestructure`, `space`, `building_floors`, `house_floor`, `direction_face`, `unit_price`, `consult_first_pay`,  `decoration_degree`, `hosedesc`,`update_time`) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);

        """
        params = (self["id"], self["title"], self["community_id"], self["community_name"], self["area1"], self["area2"],
                  self["build_time"],self["address"],  self["housetype"], self["housestructure"], self["space"],
                  self["building_floors"], self["house_floor"], self["direction_face"], self["unit_price"],
                  self["consult_first_pay"], self["decoration_degree"], '111',self['now_time'])

        return insert_sql, params
