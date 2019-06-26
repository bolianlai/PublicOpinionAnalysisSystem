# -*- coding: utf-8 -*-
BOT_NAME = 'crawl'

SPIDER_MODULES = ['crawl.spiders']
NEWSPIDER_MODULE = 'crawl.spiders'

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2

TELNETCONSOLE_ENABLED = False

SCHEDULER = "scrapy_redis.scheduler.Scheduler"

DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"

SCHEDULER_PERSIST = True

DOWNLOADER_MIDDLEWARES = {
    # 'crawl.middlewares.CustomUserAgentMiddleware': 126,
    'crawl.middlewares.CustomCookiesMiddleware': 554,
    'crawl.middlewares.CrawlDownloaderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware':123,
    'crawl.middlewares.CustomProxyMiddleware' : 125    
}

EXTENSIONS = {
   'scrapy.extensions.telnet.TelnetConsole': None,
}

ITEM_PIPELINES = {
   'crawl.pipelines.CrawlPipeline': 300,
}


RETRY_HTTP_CODES = [401, 403, 408, 414, 418, 500, 502, 503, 504]

# ----------------------------- log ----------------
import copy

from colorlog import ColoredFormatter
import scrapy.utils.log

color_formatter = ColoredFormatter(
    (
        '%(log_color)s%(levelname)-5s%(reset)s '
        '%(yellow)s[%(asctime)s]%(reset)s'
        '%(white)s %(name)s %(funcName)s %(bold_purple)s:%(lineno)d%(reset)s '
        '%(log_color)s%(message)s%(reset)s'
    ),
    datefmt='%y-%m-%d %H:%M:%S',
    log_colors={
        'DEBUG': 'blue',
        'INFO': 'bold_cyan',
        'WARNING': 'red',
        'ERROR': 'bg_bold_red',
        'CRITICAL': 'red,bg_white',
    }
)

_get_handler = copy.copy(scrapy.utils.log._get_handler)

def _get_handler_custom(*args, **kwargs):
    handler = _get_handler(*args, **kwargs)
    handler.setFormatter(color_formatter)
    return handler

scrapy.utils.log._get_handler = _get_handler_custom
# LOG_LEVEL = 'INFO'

# ----------------------------- Load .env --------------------
import os
import dotenv
dotenv.load_dotenv(dotenv.find_dotenv('.env'))
# configuration
PROXY_URL = os.getenv('PROXY_URL')
COOKIES_URL = os.getenv('COOKIES_URL')
KAFKA_SERVERS = os.getenv('KAFKA_SERVERS')
REDIS_URL = os.getenv('REDIS_URL')


# start_api
WEIBO_START_API = os.getenv('WEIBO_START_API')