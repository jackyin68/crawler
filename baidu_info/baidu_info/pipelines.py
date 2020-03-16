# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql import cursors
from twisted.enterprise import adbapi
import copy


class BaiduInfoPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'baidu',
            'charset': 'utf8',
        }
        self.conn = pymysql.connect(**dbparams)
        self.cursor = self.conn.cursor()
        self._sql = None

    def process_item(self, item, spider):
        self.cursor.execute(self.sql, (item['title'], item['abstract'], item['link']))
        self.conn.commit()
        return item

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into person_info(id,title,abstract,link,content) values (null,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql


class BaiduInfoTwistedPipeline(object):
    def __init__(self):
        dbparams = {
            'host': '127.0.0.1',
            'port': 3306,
            'user': 'root',
            'password': 'root',
            'database': 'baidu',
            'charset': 'utf8',
            'cursorclass': cursors.DictCursor,
        }
        self.dbpool = adbapi.ConnectionPool('pymysql', **dbparams)
        self._sql = None

    @property
    def sql(self):
        if not self._sql:
            self._sql = """
            insert into person_info(id,title,abstract,link, content) values (null,%s,%s,%s,%s)
            """
            return self._sql
        return self._sql

    def process_item(self, item, spider):
        asyn_item = copy.deepcopy(item)
        item_info = {
            'title': asyn_item['title'],
            'abstract': asyn_item['abstract'],
            'link': asyn_item['link'],
            'content': asyn_item['content'],
        }
        defer = self.dbpool.runInteraction(self.insert_item, item_info)
        defer.addErrback(self.handle_error, item_info, spider)

        return item

    def insert_item(self, cursor, item):
        # print(f"=============title: {item['title']}")
        # print(f"abstract: {item['abstract']}")
        # print(f"link: {item['link']}")
        cursor.execute(self.sql, (item["title"], item["abstract"], item["link"], item["content"]))

    def handle_error(self, error, item, spider):
        print(f"BaiduInfoTwistedPipeline====> error: {error}")
