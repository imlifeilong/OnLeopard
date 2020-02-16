# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
from scrapy.utils.project import get_project_settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities

import platform
import os
import time

settings = get_project_settings().copy()


class BlongSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class BlongDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        if spider.config['selenium_actions']:
            spider.driver.get(request.url)
            html = spider.driver.page_source

            return scrapy.http.HtmlResponse(
                url=request.url,
                body=html.encode('utf-8'),
                encoding='utf-8',
                request=request
            )
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest

        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SeleniumMiddleware(object):
    chromedriver = None

    def process_request(self, request, spider):
        if spider.config['selenium_actions']:
            self.driver.get(request.url)
            html = self.driver.page_source
            return scrapy.http.HtmlResponse(
                url=request.url,
                body=html.encode('utf-8'),
                encoding='utf-8',
                request=request
            )

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # self.driver.close()
        # self.driver.quit()
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        # # 代理
        # service_args = [
        #     '--proxy=%s' % 'http://http-dyn.abuyun.com:9020',
        #     '--proxy-auth=%s' % 'HQL0X344V823846D:9C4DD3099C01FD93',
        # ]
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

        if platform.system() == 'Linux':
            self.chromedriver = os.path.join(settings['BASE_DIR'], 'tools/linux/chromedriver')
        elif platform.system() == 'Windows':
            self.chromedriver = os.path.join(settings['BASE_DIR'], 'tools\windows\chromedriver.exe')
        self.driver = webdriver.Chrome(
            executable_path=self.chromedriver,
            options=chrome_options,
            # service_args=service_args
        )
