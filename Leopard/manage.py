from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging
from scrapy.utils.project import get_project_settings


def st():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    for s in ['crawler', ]:
        process.crawl(s)
    process.start()


class MyTest(object):

    def __new__(cls):
        cls.name = 'lifeilong'
        print('__new__')
        return super(MyTest, cls).__new__(cls)
        # return object.__new__(cls)

    def __init__(self):
        print(self.name)
        print('__init__')

    def __call__(self, x):
        print('__call__', x)

    def start(self):
        print('start')

if __name__ == '__main__':
    st()
    # mt = MyTest()
    # mt('s')
    # mt.start()