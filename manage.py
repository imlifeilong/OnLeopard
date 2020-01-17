# coding:utf-8

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

spider_list = [
    'SegmentFaultSpider',
]

settings = get_project_settings().copy()


def crawl(spider_names):
    process = CrawlerProcess(settings)
    for spider in spider_names:
        process.crawl(spider)
    process.start()


if __name__ == '__main__':
    crawl(spider_list)
