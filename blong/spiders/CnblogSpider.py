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
        super(CnblogSpider, self).parse(response)
        self.content_xpath = '//div[@id="post_list"]//div[@class="post_item"]'
        self.title_xpath = './/div[@class="post_item_body"]//h3/a/text()'
        # for row in response.xpath('//div[@id="post_list"]//div[@class="post_item"]'):
        #     title = row.xpath('.//div[@class="post_item_body"]//h3/a/text()').extract_first()
        #     print(title)
