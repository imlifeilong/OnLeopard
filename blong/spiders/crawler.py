# import scrapy
# from scrapy_redis.spiders import RedisSpider
#
# from Leopard.items import LeopardItem
# from Leopard.spiders.loader import LeopardItemLoader
#
# class Crawler(scrapy.Spider):
#     name = 'crawler'
#     start_urls = [
#         'http://sousuo.gov.cn/column/30469/0.htm'
#     ]
#
#     def start_requests(self):
#         url = self.start_urls[0]
#         # print('+++++++++++++++++++++++++>', url, globals())
#         yield scrapy.Request(url=url, callback=self.parse)
#
#     def parse(self, response):
#
#         for row in response.xpath('//ul[@class="listTxt"]//li//h4'):
#             loader = LeopardItemLoader(item=LeopardItem(), selector=row, response=response)
#             loader.add_xpath('date', 'span/text()')
#             loader.add_xpath('link', 'a/@href')
#             loader.add_xpath('title', 'a/text()')
#             item = loader.load_item()
#             item['date'] = item['date'].strip('[]')
#             yield item
#
# class RedisCrawler(RedisSpider):
#     name = 'redisbaiduspider'
#     redis_key = 'redisbaiduspider:start_urls'
#
#     def __init__(self, *args, **kwargs):
#         super(RedisCrawler, self).__init__(*args, **kwargs)
#
#     def parse(self, response):
#         for row in response.xpath('//ul[@class="listTxt"]//li//h4'):
#             loader = LeopardItemLoader(item=LeopardItem(), selector=row, response=response)
#             loader.add_xpath('date', 'span/text()')
#             loader.add_xpath('link', 'a/@href')
#             loader.add_xpath('title', 'a/text()')
#             item = loader.load_item()
#             item['date'] = item['date'].strip('[]')
#             yield item
