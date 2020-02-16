# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BlongItem(scrapy.Item):
    '''
        title 标题
        name 网址名
        link 链接
        author 作者
        tag 标签
        start_link 标签链接
        reads 阅读量
        posted 发布时间
        content 内容
        clicks 点赞数
    '''
    add_time = scrapy.Field()
    update_time = scrapy.Field()
    title = scrapy.Field()
    name = scrapy.Field()
    spider = scrapy.Field()
    website = scrapy.Field()
    author = scrapy.Field()
    tag = scrapy.Field()
    link = scrapy.Field()
    reads = scrapy.Field(serializer=int)
    posted = scrapy.Field()
    content = scrapy.Field()
    clicks = scrapy.Field(serializer=int)
    labels = scrapy.Field()
