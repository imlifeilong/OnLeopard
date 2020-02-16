from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities
import scrapy
import platform
import os
from scrapy.utils.project import get_project_settings
from scrapy import signals
from blong.libs import parse_config
from blong.libs import BlongItemLoader

settings = get_project_settings().copy()


class BaseSpider(scrapy.Spider):
    dirver = None
    chromedriver = None

    def __init__(self, name=None):
        super().__init__(name)
        self.config = parse_config(self.name)
        print(self.config)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = cls(*args, **kwargs)
        spider._set_crawler(crawler)
        crawler.signals.connect(spider.open_spider, signals.spider_opened)
        crawler.signals.connect(spider.close_spider, signals.spider_closed)
        return spider

    def open_spider(self):
        chrome_options = Options()
        # 无头模式
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        # 不调用Java
        chrome_options.add_argument('–disable-java')
        # 拦截弹出
        chrome_options.add_argument('–disable-popup-blocking')
        # 不打开应用页
        chrome_options.add_argument('--no-sandbox')
        # 单进程
        chrome_options.add_argument('–single-process')
        # 无痕模式
        chrome_options.add_argument('–incognito')

        # 禁止图片和css加载
        chrome_options.add_experimental_option("prefs", {
            'profile.managed_default_content_settings.images': 2,
            # 'profile.managed_default_content_settings.javascript': 2,
            'permissions.default.stylesheet': 2
        })

        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["pageLoadStrategy"] = "none"

        if platform.system() == 'Linux':
            self.chromedriver = os.path.join(settings['BASE_DIR'], 'tools/linux/chromedriver')
        elif platform.system() == 'Windows':
            self.chromedriver = os.path.join(settings['BASE_DIR'], 'tools\windows\chromedriver.exe')

        self.driver = webdriver.Chrome(
            executable_path=self.chromedriver,
            options=chrome_options,
            # service_args=service_args
        )

    def close_spider(self):
        self.driver.close()
        self.driver.quit()
        self.driver = None
        self.chromedriver = None

    def start_requests(self):
        self.start_urls = {item['tag']: item['start_link'] for item in self.config['start_urls']}
        if self.start_urls:
            for url in self.start_urls.items():
                yield scrapy.Request(url=url[1], meta={'tag': url[0]})

    def parse(self, response):
        yield from self.parse_list(response)
        _next = response.xpath(self.config['next']).extract_first()
        if _next:
            if not _next.startswith('http'):
                _next = self.config['website'] + _next

            yield from self.parse_next(response, _next)

    def parse_list(self, response):
        for row in response.xpath(self.config['list']):
            loader = BlongItemLoader(selector=row, response=response)
            for key, value in self.config['item'].items():
                loader.add_xpath(key, value)
            item = loader.load_item()
            item['tag'] = response.meta['tag']
            yield scrapy.Request(
                url=item['link'],
                # url='https://www.cnblogs.com/xiaoyangjia/p/11535486.html',
                callback=self.parse_single,
                dont_filter=True,
                meta={'item': item}
            )

    def parse_single(self, response):
        # print(response.meta['item'])
        loader = BlongItemLoader(response.meta['item'], response=response)
        # labels = response.xpath('//div[@id="blog_post_info_block"]//div[@id="EntryTag"]')
        # print(labels)

        for key, value in self.config['single'].items():
            # if key.startswith('content'): continue
            loader.add_xpath(key, value)
        item = loader.load_item()

        item['website'] = self.config['website']
        item['name'] = self.config['name']
        item['spider'] = self.config['spider']

        print('--------->', item['title'])
        yield item

    def parse_next(self, response, _next):
        # print('next===============>', response, _next)
        yield scrapy.Request(
            url=_next,
            callback=self.parse,
            meta=response.meta
        )
