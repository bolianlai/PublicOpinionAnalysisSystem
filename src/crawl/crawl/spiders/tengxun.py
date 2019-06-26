# -*- coding: utf-8 -*-
import scrapy


class TengxunSpider(scrapy.Spider):
    name = 'tengxun'
    allowed_domains = ['qq.com']
    start_urls = ['http://qq.com/']

    def parse(self, response):
        pass
