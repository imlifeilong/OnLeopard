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
        item['labels'] = '' if 'labels' not in item else item['labels']
        select_sql = '''SELECT * FROM blongs where link='%s';''' % item['link']
        # item['content'] = pymysql.escape_string(item['content'])
        item['content'] = ''
        item['author'] = pymysql.escape_string(item['author'])
        item['title'] = pymysql.escape_string(item['title'])
        item['update_time'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.cursor.execute(select_sql)

        # 当天发布
        if not item['posted']:
            item['posted'] = time.strftime("%Y-%m-%d", time.localtime())

        if self.cursor.rowcount == 0:
            item['add_time'] = item['update_time']
            # 入库文章
            insert_sql = '''INSERT INTO blongs.blongs (`add_time`, `update_time`, `website`, `author`, 
            `content`, `link`, `clicks`, `posted`, `title`, `tag`, `reads`, `labels`, `name`, `spider`) 
            VALUES ('{add_time}', '{update_time}', '{website}', '{author}', '{content}', '{link}', 
            {clicks}, '{posted}', '{title}', '{tag}', {reads}, '{labels}', '{name}', '{spider}');'''.format(**item)

            self.cursor.execute(insert_sql)

        else:
            update_sql = '''UPDATE blongs.blongs SET `update_time`='{update_time}', `content`='{content}', `clicks`={clicks}, `reads`={reads} WHERE `link`='{link}';'''.format(
                **item)
            # print(update_sql)
            self.cursor.execute(update_sql)
        # 提交
        self.client.commit()
        return item
