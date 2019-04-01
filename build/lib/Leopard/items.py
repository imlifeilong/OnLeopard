# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

def my_se(s):
    print('===========================================>', type(s))
    return str(s)


class LeopardItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    # 序列化为字符串
    date = scrapy.Field(serializer=my_se)
    link = scrapy.Field()
