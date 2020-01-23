import scrapy
import re
from blong.spiders.base import BaseSpider


class CnblogSpider(BaseSpider):
    name = 'CnblogSpider'
    base_url = 'https://www.cnblogs.com'
    start_urls = [
        'https://www.cnblogs.com/cate/python/'
    ]

    def parse(self, response):
        self.content_xpath = '//div[@id="post_list"]//div[@class="post_item"]'
        self.title_xpath = './/div[@class="post_item_body"]//h3/a/text()'
        self.link_xpath = './/div[@class="post_item_body"]//h3/a/@href'
        super(CnblogSpider, self).parse(response)
