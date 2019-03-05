# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QiushuItem(scrapy.Item):
    # define the fields for your item here like:
    # 书名
    name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 书籍分类标签
    booktype = scrapy.Field()
    # 书籍状态
    state = scrapy.Field()
    # 书籍的有效地址
    showUrl = scrapy.Field()
    # 图片链接
    tuurl = scrapy.Field()
    # 书籍描述
    describe = scrapy.Field()
    # 章节名
    chapter = scrapy.Field()
    # 章节
    chapterurl = scrapy.Field()

