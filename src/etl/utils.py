import time
import re
import logging
from datetime import datetime, timedelta
import happybase
from confluent_kafka import Consumer, Producer
import pymysql
from DBUtils.PooledDB import PooledDB, SharedDBConnection
from DBUtils.PersistentDB import PersistentDB, PersistentDBError, NotSupportedError
logger = logging.getLogger(__name__)
import dotenv
import os
import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from operator import add
import json


dotenv.load_dotenv(dotenv.find_dotenv('.env'))
HBASE_CONF_HOST = os.getenv('HBASE_CONF_HOST')
HBASE_CONF_TABLE_PREFIX = os.getenv('HBASE_CONF_TABLE_PREFIX')
HBASE_CONF_SIZE = os.getenv('HBASE_CONF_SIZE')

MYSQL_CONF = os.getenv('MYSQL_CONF')


KAFKA_CONSUMER_CONF = os.getenv('KAFKA_CONSUMER_CONF')
KAFKA_PRODUCER_CONF = os.getenv('KAFKA_PRODUCER_CONF')
# hbasepool = happybase.ConnectionPool(size=int(HBASE_CONF_SIZE), host=HBASE_CONF_HOST, table_prefix=HBASE_CONF_TABLE_PREFIX)
# mysqlpool = PooledDB(creator=pymysql, blocking=True,  ping=0, **MYSQL_CONF)


# 格式化时间成时间戳，例如：几分钟前、几天前、几小时前
def transform_time(starttime, created_at):
    if u'刚刚' in created_at:
        return str(int(time.time()))
    current_year = datetime.today().strftime("%Y")
    result = re.findall('\d+', created_at)
    if not result:
        return False
    num = int(result[0])
    if u'秒' in created_at:
        s = (datetime.fromtimestamp(starttime) - timedelta(seconds=num))
    elif u'分钟前' in created_at:
        s = (datetime.fromtimestamp(starttime) - timedelta(minutes=num))

    elif u'小时前' in created_at:
        s = (datetime.fromtimestamp(starttime) - timedelta(hours=num))
    elif u'天前' in created_at:
        s = (datetime.fromtimestamp(starttime) - timedelta(days=num))
    elif len(re.findall('-', created_at)) == 1:
        created_at += ", " + current_year
        s = datetime.strptime(created_at, "%m-%d, %Y")
    elif len(re.findall('-', created_at)) == 2:
        s = datetime.strptime(created_at, "%Y-%m-%d")
    else:
        return created_at
    return str(int(time.mktime(s.timetuple())))

# 根据话题为文件名保存成文件
def save_to_file(data, filename):
    with open('data/{}.txt'.format(filename), 'a', encoding='utf-8') as f:
        f.writelines(data)

# 保存数据到hbase
# def save_to_hbase(data, row, family):
#     # 使用连接池
#     # 获取连接
#     with hbasepool.connection() as connection:
#         # # # 禁用表
#         # connection.disable_table(b'weibo')
#         # # 删除表
#         # connection.delete_table(b'weibo', disable=False)

#         if b'weibo' not in connection.tables():
#             connection.create_table(
#                 b'weibo',
#                 {
#                     'WeiboTitleTop': dict(),
#                     'WeiboContentList': dict(),
#                     'WeiboComments': dict(),
#                     'WeiboTopic': dict(),
#                 }
#             )
#         if not connection.is_table_enabled(b'weibo'):
#             connection.enable_table(b'weibo')

#         table = connection.table(b'weibo')
#         with table.batch() as bat:
#             bat.put(str(row), data)

# # 保存数据到mysql
# def save_to_mysql(data, sql):
#     conn = mysqlpool.connection()
#     cursor = conn.cursor()
#     cursor.execute(sql)
#     conn.close()

# 从kafka中获取数据
def get_form_kafka(topic, conf=None):
    '''
    和kafka建立连接，获取其中的数据并返回
    '''
    # conf = conf if conf else KAFKA_CONSUMER_CONF
    conf = {
        'bootstrap.servers': '127.0.0.1:9091',
        'group.id': 'etl',
        'enable.auto.commit': False,
        'default.topic.config': {
            'auto.offset.reset': 'earliest',
        }
    }
    consumer = Consumer(conf)
    consumer.subscribe([topic])
    while True:
        msg = consumer.poll(1)
        if msg is None:
            continue
        if msg.error():
            consumer.close()
            return False
        yield msg.value().decode('utf-8')

# 将数据保存到kafka
def save_to_kafka(data, topic, conf=None):
    '''
    和kafka建立连接，将数据保存到其中
    '''
    conf = conf if conf else KAFKA_PRODUCER_CONF
    producer = Producer(**conf)
    def delivery_callback(err, msg):
        if err:
            logger.error('Message failed delivery: %s\n' % err)
        else:
            logger.debug('Message delivered to %s [%d] @ %d\n' % (msg.topic(), msg.partition(), msg.offset()))
        try:
            producer.produce(topic, value=data, callback=delivery_callback)
        except BufferError as e:
            logger.error('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(producer))    
        producer.poll(0)
        producer.flush()

# 创建sparkstream和kafka连接,并返回实例对象
def create_sparkstreaming(kafkatopic, master=None, appname=3, kafkabrokers='127.0.0.1:9091', ):
    sc = SparkContext(master=master, appName=appname)
    ssc = StreamingContext(sc, 5)
    kvs = KafkaUtils.createDirectStream(ssc, [kafkatopic], {"metadata.broker.list": kafkabrokers})
    return ssc


def analysis(data):

    pass