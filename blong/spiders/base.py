import scrapy


class BaseSpider(scrapy.Spider):
    base_url = None
    content_xpath = None
    link_xpath = None
    title_xpath = None
    tag_xpath = None

    items = ('title', 'link', 'tag', 'website', 'author', 'content', 'clicks', 'publish_date')

    # def parse_xpath(self):
    #     for item in self.items:
    #         if hasattr(self, item + '_xpaht'):

    def parse(self, response):
        self.crawler.stats.set_value('spider_name', self.name)

        for row in response.xpath(self.content_xpath):
            link = row.xpath(self.link_xpath).extract_first()
            title = row.xpath(self.title_xpath).extract_first()
            tag = row.xpath(self.tag_xpath).extract_first()

            yield scrapy.Request(
                url=self.base_url + link,
                callback=self.parse_single,
                dont_filter=True,
                meta={'data': {'title': title, 'link': self.base_url + link, 'tag': tag}},
            )
            pass

    # def request_single(self, url, callback, meta):
    #     scrapy.Request(
    #         url=self.base_url + link,
    #         callback=self.parse_single,
    #         dont_filter=True,
    #         meta={'data': {'title': title, 'link': self.base_url + link, 'tag': tag}},
    #     )

    def parse_single(self, response):
        pass

    @staticmethod
    def parse_tag(txt):
        pass
