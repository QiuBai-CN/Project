# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewHouseItem(scrapy.Item):
    province = scrapy.Field() #省份
    city = scrapy.Field() #城市
    name = scrapy.Field() #小区名字
    price = scrapy.Field() #价格
    rooms = scrapy.Field() #居室
    area = scrapy.Field() #房子面积
    address = scrapy.Field() #房子地址
    district = scrapy.Field() #行政区
    sale = scrapy.Field() #是否在售
    origin_url = scrapy.Field() #详情页面URL


