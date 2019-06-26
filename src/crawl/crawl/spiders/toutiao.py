# -*- coding: utf-8 -*-
import scrapy


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = ['toutiao.com']
    start_urls = ['http://toutiao.com/']

    def parse(self, response):
        pass
