import json
import re
from datetime import datetime, timedelta
import time
import utils
from snownlp import SnowNLP

record = 0

def cleandata(data):
    global record
    for d in data:
        result = json.loads(d)
        topic = ''.join(re.findall('-#(.*?)#', result.get('data').get('cardlistInfo').get('title_top')))
        starttime = result.get('data').get('cardlistInfo').get('starttime')

        for r in  result.get('data').get('cards')[0].get('card_group'):
            content_id = r.get('mblog').get('id')
            url = 'https://m.weibo.cn/detail/' + content_id
            created_at = utils.transform_time(starttime, r.get('mblog').get('created_at'))
            content = r.get('mblog').get('text') if not r.get('mblog').get('isLongText') else r.get('mblog').get('longText').get('longTextContent')
            dr = re.compile(r'<[^>]+>', re.S) 
            content = dr.sub('', content) 
            source = '<{}>'.format(r.get('mblog').get('source'))
            reposts_count = r.get('mblog').get('reposts_count')
            comments_count = r.get('mblog').get('comments_count')
            attitudes_count = r.get('mblog').get('attitudes_count')
            user_id = r.get('mblog').get('user').get('id')

            content = content.replace('\n', '').replace(topic, '').replace('#', '')
            print('#:{}'.format(record))
            record +=1
            # mysqldata = {
            #         'title': content[:100] if 100 < len(content) else content,
            #         'intro': content[:200] if 100 < len(content) else content,
            #         'content_url': url, 
            #         'content_from': '新浪微博',
            #         'media_type': '微博',
            #         'lyric_attribute': str(attitudes_count),
            #         'url': url,
            #         'WeiboContentList:user_id': str(user_id),
            #         'content': content
            # }
            s = SnowNLP(content)
            print('分析结果：', s.sentiments)

            utils.save_to_file(data=str(s.sentiments) + ':::::' + content + '\n', filename=topic)

if __name__ == "__main__":
    data = utils.get_form_kafka(topic='WeiboContentList')
    cleandata(data)
    for d in data:
        print(d)

        #     sql = ''
        #     yield utils.save_to_mysql(data, sql)
        #     yield utils.save_to_hbase(hbasedata, row=starttime, family=topic)
 #     mysqldata = {
        #             'title': content[:100] if 100 < len(content) else content,
        #             'intro': content[:200] if 100 < len(content) else content,
        #             'content_url': url, 
        #             'content_from': '新浪微博',
        #             'media_type': '微博',
        #             'lyric_attribute': str(attitudes_count),
        #             'url': url,
        #             'WeiboContentList:user_id': str(user_id),
        #             'content': content
        #     }

        #     hbasedata = {
        #             'WeiboContentList:content_id': str(content_id),
        #             'WeiboContentList:created_at': str(created_at),
        #             'WeiboContentList:source': source, 
        #             'WeiboContentList:reposts_count': str(reposts_count),
        #             'WeiboContentList:comments_count': str(comments_count),
        #             'WeiboContentList:attitudes_count': str(attitudes_count),
        #             'WeiboContentList:url': url, 
        #             'WeiboContentList:user_id': str(user_id),
        #             'WeiboContentList:content': content
        #     }
