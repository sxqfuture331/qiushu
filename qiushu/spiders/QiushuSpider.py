# -*- coding: utf-8 -*-
import scrapy
import time
from qiushu.items import QiushuItem

class QiushuspiderSpider(scrapy.Spider):
    name = 'QiushuSpider'
    allowed_domains = ['www.qiushu.cc']
    start_urls = ['http://www.qiushu.cc/']

    def parse(self, response):
        '''解析分类列表'''
        # TODO 解析分类
        # 分类URLs
        links = response.xpath('//p[@class="hot_tips"]/a/@href').extract()
        # 所有类型链接
        for i in links:
            url = 'http://www.qiushu.cc' + i
            yield scrapy.Request(url, callback=self.parse_books, dont_filter=True)

    def parse_books(self, response):
        '''解析书籍列表'''
        # TODO： 解析书籍列表
        # time.sleep(2)
        book_url = []
        for i in response.xpath('//*[@id="main"]/div[1]/div/div/ul/li'):
            book_dan_url = ''.join(i.xpath('.//span[@class="t1"]/a/@href').extract_first())
            book_url.append(book_dan_url)
            # print('*' * 30, book_dan_url)
        # print('*' * 30, book_url)
        for i in book_url:
            yield scrapy.Request(i, callback=self.parse_section, dont_filter=True)
        # TODO: 处理下一页
        xia_url = ''.join(response.xpath('//*[@class="next"]/@href').extract())
        if bool(xia_url):
            yield scrapy.Request(xia_url, callback=self.parse_books, dont_filter=True)


    def parse_section(self, response):
        item = QiushuItem()
        # 书名
        item['name'] = ''.join(response.xpath('//div[@class="title"]/h1/text()').extract())
        # 作者
        item['author'] = ''.join(response.xpath('//div[@class="title"]/span/text()').extract())
        # 书籍分类标签
        item['booktype'] = ''.join(response.xpath('//*[@id="main"]/div[2]/text()[2]').extract()).split('>')[1]
        # 书籍状态
        item['state'] = ''.join(response.xpath('//*[@id="main"]/div[2]/span/text()').extract())
        # 书籍的有效地址
        item['showUrl'] = response.url
        # 书记封面
        item['tuurl'] = ''.join(response.xpath('//div[@class="book_cover"]/img/@src').extract())
        # 书籍描述
        item['describe'] = ''.join(response.xpath('//div[@class="intro"]/p/text()').extract())
        
        nei_zong = []
        nei_zong_url = []
        for i in response.xpath('//div[@class="book_con_list"][2]/ul'):
            for jj in i.xpath('./li'):
                nei_url = response.url + ''.join(jj.xpath('./a/@href').extract_first())
                nei = jj.xpath('./a/text()').extract_first()
                nei_zong_url.append(nei_url)
                nei_zong.append(nei)
                # import ipdb as pdb; pdb.set_trace()
                print(nei , nei_url)
        # 章节名
        item['chapter'] = nei_zong
        # 章节
        item['chapterurl'] = nei_zong_url
        yield item
