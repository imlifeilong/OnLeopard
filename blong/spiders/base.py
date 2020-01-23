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
            link = self.parse_link(row)
            title = row.xpath(self.title_xpath).extract_first()

            yield scrapy.Request(
                url=self.base_url + link,
                callback=self.parse_single,
                dont_filter=True,
                meta={'data': {'title': title, 'link': link}},
            )

    def parse_link(self, row):
        href = row.xpath(self.link_xpath).extract_first()
        if href.startswith('http'):
            return href
        else:
            return self.base_url + href

    @staticmethod
    def parse_tag(tag):
        pass

    def parse_website(self):
        return self.base_url

    def parse_single_author(self, response):
        pass

    def parse_single_clicks(self, response):
        pass

    def parse_single_date(self, response):
        pass

    def parse_single_content(self, response):
        pass
