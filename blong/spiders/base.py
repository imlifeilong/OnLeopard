import scrapy
from blong.libs import parse_config
from blong.libs import BlongItemLoader


# class BaseSpider(scrapy.Spider):
#     base_url = None
#     content_xpath = None
#     link_xpath = None
#     title_xpath = None
#     tag_xpath = None
#
#     items = ('title', 'link', 'tag', 'website', 'author', 'content', 'clicks', 'publish_date')
#
#     # def parse_xpath(self):
#     #     for item in self.items:
#     #         if hasattr(self, item + '_xpaht'):
#
#     def parse(self, response):
#         self.crawler.stats.set_value('spider_name', self.name)
#
#         for row in response.xpath(self.content_xpath):
#             link = self.parse_link(row)
#             title = row.xpath(self.title_xpath).extract_first()
#
#             yield scrapy.Request(
#                 url=self.base_url + link,
#                 callback=self.parse_single,
#                 dont_filter=True,
#                 meta={'data': {'title': title, 'link': link}},
#             )
#
#     def parse_link(self, row):
#         href = row.xpath(self.link_xpath).extract_first()
#         if href.startswith('http'):
#             return href
#         else:
#             return self.base_url + href
#
#     @staticmethod
#     def parse_tag(tag):
#         pass
#
#     def parse_single(self, response):
#         pass
#
#     def parse_website(self):
#         return self.base_url
#
#     def parse_single_author(self, response):
#         pass
#
#     def parse_single_clicks(self, response):
#         pass
#
#     def parse_single_date(self, response):
#         pass
#
#     def parse_single_content(self, response):
#         pass


class BaseSpider(scrapy.Spider):
    def __init__(self, name=None):
        super().__init__(name)
        self.config = parse_config(self.name)
        print(self.config)

    def start_requests(self):
        self.start_urls = self.config['start_urls']
        if self.start_urls:
            for url in self.start_urls:
                yield scrapy.Request(url=url['start_link'])

    def parse(self, response):
        yield from self.parse_list(response)
        _next = response.xpath(self.config['next'])
        if _next:
            yield from self.parse_next(response)

    def parse_list(self, response):
        for row in response.xpath(self.config['list']):
            loader = BlongItemLoader(selector=row, response=response)
            for key, value in self.config['item'].items():
                loader.add_xpath(key, value)
            item = loader.load_item()
            #
            # print(item)
            yield scrapy.Request(
                url=item['link'],
                callback=self.parse_single,
                dont_filter=True,
                meta={'data': loader}
            )

    def parse_single(self, response):
        print('single------------>', response)
        yield

    def parse_next(self, response):
        print('next===============>', response)
        yield
