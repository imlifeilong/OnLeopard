# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import time


class DB(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(DB, cls).__new__(cls)
        return cls._instance

    def __init__(self, connect):
        self.connect = connect

    def __enter__(self):
        self.client = pymysql.connect(**self.connect)
        self.cursor = self.client.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()
        self.cursor.close()

    def execute_cursor(self, sql):
        self.cursor.execute(sql)
        return self.cursor

    def cursor_(self):
        return self.cursor

    def select_(self, sql):
        return self.execute_cursor(sql)

    def insert_(self, select_sql, insert_sql):
        if self.select_(select_sql).rowcount == 0:
            self.execute_cursor(insert_sql)
            self.client.commit()


class BlongPipeline(object):
    def process_item(self, item, spider):
        return item


class MysqlPipeline(object):
    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         cls._instance = super(DB, cls).__new__(cls, *args, **kwargs)
    #     return cls._instance

    def __init__(self, connect):
        self.connect = connect

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            connect=crawler.settings.get('MYSQLCON'),
        )

    def open_spider(self, spider):
        self.client = pymysql.connect(**self.connect)
        self.cursor = self.client.cursor()

    def close_spider(self, spider):
        self.cursor.close()
        self.client.close()


    def process_item(self, item, spider):

        select_sql = '''SELECT * FROM pyblongs where link='%s';''' % item['link']
        item['content'] = pymysql.escape_string(item['content'])
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cursor.execute(select_sql)

        # 当天发布
        if not item['publish_date']:
            item['publish_date'] = time.strftime("%Y-%m-%d", time.localtime())

        if self.cursor.rowcount == 0:
            item['add_time'] = item['update_time']
            insert_sql = '''INSERT INTO blongs.pyblongs VALUES ('{add_time}', '{update_time}', '{website}', '{author}', '{content}', '{link}', '{clicks}', '{publish_date}', '{title}', '{tag}');'''.format(**item)
            self.cursor.execute(insert_sql)

        else:
            update_sql = '''UPDATE blongs.pyblongs SET update_time='{update_time}', content='{content}', clicks='{clicks}', publish_date='{publish_date}', tag='{tag}' WHERE (link='{link}');'''.format(**item)
            self.cursor.execute(update_sql)
        # 提交
        self.client.commit()
        return item
