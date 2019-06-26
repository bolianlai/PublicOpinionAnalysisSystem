# import redis

# pool = redis.ConnectionPool.from_url('redis://:yourpassword@127.0.0.1/2')
# rc = redis.StrictRedis(connection_pool=pool)
# ps = rc.pubsub()
# ps.subscribe(['crawl_list'])
# print('ps:', ps)
# for item in ps.listen():
#     print('#',item)
#     # if item['type'] == 'message':
#     #     print(item['channel'] , item['data'])

import redis

pool = redis.ConnectionPool.from_url('redis://:yourpassword@127.0.0.1/2')
r = redis.StrictRedis(connection_pool=pool)

p = r.pubsub()
# p.subscribe(['crawl_list:tieba'])
p.psubscribe(['crawl_list*'])

for item in p.listen():
    if item['type'] == 'pmessage' or item['type'] == 'message':
        print(item['channel'])
        print(item['data'])
        # p.unsubscribe('test2')