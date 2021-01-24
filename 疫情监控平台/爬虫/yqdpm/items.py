# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DayListItem(scrapy.Item):
    # define the fields for your item here like:
    confirm = scrapy.Field()
    suspect = scrapy.Field()
    heal = scrapy.Field()
    dead = scrapy.Field()
    date = scrapy.Field()
    confirm_add = scrapy.Field()
    suspect_add = scrapy.Field()
    heal_add = scrapy.Field()
    dead_add = scrapy.Field()

class CityInfoItem(scrapy.Item):
    update_time = scrapy.Field()
    province_name = scrapy.Field()
    city_name = scrapy.Field()
    confirm = scrapy.Field()
    confirm_add = scrapy.Field()
    heal = scrapy.Field()
    dead = scrapy.Field()

