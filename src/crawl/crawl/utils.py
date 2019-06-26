from apscheduler.schedulers.twisted import TwistedScheduler
import os
from datetime import datetime
from .settings import REDIS_URL
import redis


class CrawlStatus():
    def __init__(self, conf):
        self.spider_name = conf.get("spider_name")
        self.seconds = conf.get("seconds")
        self.redis_key = conf.get("redis_key")
        self.start_api = conf.get("start_api")
        self.data = {"site_name": conf.get("spider_name"), "spider_name": conf.get("site_name"), "redis_key": conf.get("redis_key"), "seconds": conf.get("seconds"), "datetime": str(datetime.now()), "start_api": conf.get("start_api")}
        self.pool = redis.ConnectionPool.from_url(REDIS_URL)
        self.r = redis.StrictRedis(connection_pool=self.pool)
        self.r.set("crawl_list:{}".format(self.spider_name), str(self.data))

        # 测试用
        self.r.lpush("{}".format(self.redis_key), self.start_api)

    def crawl_status(self):
        self.data['datetime'] = str(datetime.now())
        self.r.setex("crawl_status:{}".format(self.spider_name), 5 , str(self.data))
        

    def run(self):
        scheduler = TwistedScheduler()
        scheduler.add_job(self.crawl_status, "interval", seconds=self.seconds)

        try:
            scheduler.start()
        except (KeyboardInterrupt, SystemExit):
            pass
