import redis
import time

pool = redis.ConnectionPool.from_url('redis://:yourpassword@127.0.0.1/2')
r = redis.StrictRedis(connection_pool=pool)

while True:
    time.sleep(1)
    r.publish('crawl_list:tieba', 'tieba.baidu.com')
    r.publish('crawl_list:weibo', 'm.weibo.com')
    print('####')