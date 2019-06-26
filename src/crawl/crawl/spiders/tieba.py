# -*- coding: utf-8 -*-
import scrapy


class TiebaSpider(scrapy.Spider):
    name = 'tieba'
    allowed_domains = ['tieba.com']
    start_urls = ['http://tieba.com/']

    def parse(self, response):
        pass
