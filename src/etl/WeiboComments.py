import json
import re
from datetime import datetime, timedelta
import time
import utils

def clean_data(data):
    for d in data:
        result = json.loads(d)
        topic = ''.join(re.findall('-#(.*?)#', result.get('data').get('cardlistInfo').get('title_top')))
        starttime = result.get('data').get('cardlistInfo').get('starttime')

        for r in  result.get('data').get('cards')[0].get('card_group'):
            content_id = r.get('mblog').get('id')
            url = 'https://m.weibo.cn/detail/' + content_id
            created_at = utils.transform_time(starttime, r.get('mblog').get('created_at'))
            content = r.get('mblog').get('text') if not r.get('mblog').get('isLongText') else r.get('mblog').get('longText').get('longTextContent').replace('\n', '')

            dr = re.compile(r'<[^>]+>', re.S) 
            content = dr.sub('', content) 
            source = '<{}>'.format(r.get('mblog').get('source'))
            reposts_count = r.get('mblog').get('reposts_count')
            comments_count = r.get('mblog').get('comments_count')
            attitudes_count = r.get('mblog').get('attitudes_count')
            user_id = r.get('mblog').get('user').get('id')
            
            data = {
                    'WeiboContentList:content_id': str(content_id),
                    'WeiboContentList:created_at': str(created_at),
                    'WeiboContentList:source': source, 
                    'WeiboContentList:reposts_count': str(reposts_count),
                    'WeiboContentList:comments_count': str(comments_count),
                    'WeiboContentList:attitudes_count': str(attitudes_count),
                    'WeiboContentList:url': url, 'WeiboContentList:user_id': str(user_id),
                    'WeiboContentList:content': content
            }
            # utils.save_to_file(data=data, filename=topic)
            yield utils.save_to_hbase(data, row=starttime, family=topic)

if __name__ == "__main__":
    # 获取数据
    data = utils.consumer_weibo(topic='WeiboComments')
    # 清洗数据
    clean_data(data)
