# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
import time
import urllib.parse
import re
import logging
import threading
logger = logging.getLogger(__name__)
from scrapy_redis.spiders import RedisCrawlSpider
from ..utils import CrawlStatus
from ..settings import WEIBO_START_API
import time

class WeiboSpider(RedisCrawlSpider):
    name = 'weibo'
    allowed_domains = ['m.weibo.cn', '']
    redis_key = 'weibo:start_urls'
    # start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=106003type%3D25%26t%3D3%26disable_hot%3D1%26filter_type%3Drealtimehot&title=%E5%BE%AE%E5%8D%9A%E7%83%AD%E6%90%9C&extparam=filter_type%3Drealtimehot%26mi_cid%3D100103%26pos%3D0_0%26c_type%3D30%26display_time%3D1559000036&luicode=10000011&lfid=231583',]
    content_api = 'https://m.weibo.cn/api/container/getIndex?'
    comment_api = 'https://m.weibo.cn/comments/hotflow?'
    site_name = '微博'
    seconds = 5
    start_api = WEIBO_START_API

    def __init__(self, category=None, *args, **kwargs):
        super(WeiboSpider, self).__init__(*args, **kwargs)
        timed_scheduling = CrawlStatus(conf={'site_name': self.site_name, 'spider_name': self.name,  'redis_key': self.redis_key, 'seconds': self.seconds, 'start_api': self.start_api})
        timed_scheduling.run()

    def parse(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data'):
            result['topic'] = 'WeiboTitleTop'
            yield result

            d= {
                'containerid': '100103type=61&q=#{}#&t=0',
                'isnewpage': 1,
                'extparam': 'filter_type=realtimehot&pos=0&c_type=31&realpos=0&flag=2&display_time=1559015068',
                'luicode': '10000011',
                'lfid': '106003type=25&t=3&disable_hot=1&filter_type=realtimehot',
                'page_type': 'searchall',
                'page': '1',
            }

            for r in result.get('data').get('cards')[0].get('card_group'):
                d['containerid'] = '100103type=61&q=#{}#&t=0'.format(r.get('desc'))
                content_api = self.content_api + urllib.parse.urlencode(d)
                yield {'topic': 'WeiboTopic', 'name': r.get('desc')}
                yield Request(url = content_api, callback = self.parse_weibo)

    def parse_weibo(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data'):
            result['topic'] = 'WeiboContentList'
            yield result
            
            d = dict()
            for r in result.get('data').get('cards')[0].get('card_group'):
                d['id'] = r.get('mblog').get('id')
                d['mid'] = r.get('mblog').get('mid')
                d['max_id_type'] = 0
                comment_api = self.comment_api + urllib.parse.urlencode(d)
                yield Request(url = comment_api, callback = self.parse_comment, meta = {'id': d['id'],'mid': d['mid']})

            urlparse_result = urllib.parse.parse_qs(urllib.parse.urlparse(response.url).query)
            urlparse_result['page'][0] = int(urlparse_result['page'][0]) + 1
            content_api = self.content_api + urllib.parse.urlencode(dict(zip(map(lambda x: x, urlparse_result.keys()), map(lambda x: x[0], urlparse_result.values()))))
            yield Request(url = content_api, callback = self.parse_weibo)

    def parse_comment(self, response):
        result = json.loads(response.text)
        if result.get('ok') and result.get('data'):
            result['topic'] = 'WeiboComments'
            yield result

            if result.get('data').get('max_id'):
                d = dict()
                d['id'] = response.meta['id']
                d['mid'] = response.meta['mid']
                d['max_id'] = result.get('data').get('max_id')
                d['max_id_type'] = result.get('data').get('max_id_type')
                comment_api = self.comment_api + urllib.parse.urlencode(d)
                yield Request(url = comment_api, callback = self.parse_comment, meta=response.meta)
    
    # def parse_comment_reply(self, response):
    #     result = json.loads(response.text)
    #     if result.get('comments'):
    #         result['topic'] = 'WeiboComments'
    #         yield result
            
    #     if result.get('max_id'):
    #         self.comment_reply_api_parameter['max_id'] = result.get('mad_id')
    #         self.comment_reply_api_parameter['id'] = result.get('status').get('id')
    #         comment_reply_api = self.comment_api + urllib.parse.urlencode(self.comment_reply_api_parameter)
    #         yield Request(url = comment_reply_api, callback = self.parse_comment_reply)