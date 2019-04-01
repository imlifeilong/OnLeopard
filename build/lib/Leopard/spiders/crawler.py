import scrapy
from Leopard.items import LeopardItem
from Leopard.spiders.loader import LeopardItemLoader

class Crawler(scrapy.Spider):
    name = 'crawler'
    start_urls = [
        'http://www.aheic.gov.cn/infoCol_list.jsp?strColId=13739483445468567'
    ]

    def start_requests(self):
        url = self.start_urls[0]
        # print('+++++++++++++++++++++++++>', url, globals())
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):

        for row in response.xpath('//div[@class="listrig02"]//ul//li'):
            loader = LeopardItemLoader(item=LeopardItem(), selector=row, response=response)
            loader.add_xpath('date', 'i/text()')
            loader.add_xpath('link', 'a/@href')
            loader.add_xpath('title', 'a/text()')
            item = loader.load_item()
            item['date'] = item['date'].strip('[]')
            yield item