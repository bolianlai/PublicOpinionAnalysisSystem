# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
from .settings import KAFKA_SERVERS
import logging
from confluent_kafka import Producer
import sys

class CrawlPipeline(object):
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        conf = {'bootstrap.servers': KAFKA_SERVERS,
                'message.max.bytes': 4194304,}
        self.producer = Producer(**conf)

    def process_item(self, item, spider):
        data = json.dumps(item)

        def delivery_callback(err, msg):
            if err:
                self.logger.error('Message failed delivery: %s\n' % err)
            else:
                self.logger.debug('Message delivered to %s [%d] @ %d\n' %
                                (msg.topic(), msg.partition(), msg.offset()))

        try:
            self.producer.produce(item.get('topic'), value=data, callback=delivery_callback)
        except BufferError as e:
                self.logger.error('%% Local producer queue is full (%d messages awaiting delivery): try again\n' % len(self.producer))    
        self.producer.poll(0)
        self.producer.flush()
        return item
