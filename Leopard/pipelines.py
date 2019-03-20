# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql

# class LeopardPipeline(object):
#     def process_item(self, item, spider):
#         return item


class MySQLPipeline(object):
    def __init__(self, *args, **kwargs):
        self.connect = pymysql.connect(host='127.0.0.1', port=3306, db='leo', user='root', passwd='123456', charset='utf8')
        self.cur = self.connect.cursor()

    def process_item(self, item, spider):
        sql = '''INSERT INTO `leo`.`leob` (`date`, `title`, `link`) VALUES ('%s', '%s', '%s');''' % (item['date'], item['title'], item['link'])

        self.cur.execute(sql)
        self.connect.commit()
        return item