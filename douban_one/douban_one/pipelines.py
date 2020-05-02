# -*- coding: utf-8 -*-
import pymongo
from douban_one.items import DoubanUserItem, UserRelationItem, UserEventsItem, EventItem, EventUsersItem
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class MongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db[DoubanUserItem.collection].create_index([('id', pymongo.ASCENDING)])
        self.db[EventItem.collection].create_index([('id', pymongo.ASCENDING)])


    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item, DoubanUserItem):         #在mongodb中加入用户基本信息
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)

        elif isinstance(item, UserRelationItem):         #在mongodb中加入用户粉丝和关注信息
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':
                    {
                        'follows': {'$each': item.get('follows')},
                        'fans': {'$each': item['fans']}
                    }
                }, True)

        elif isinstance(item, UserEventsItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':
                     {
                         'attend_events':{'$each': item.get('attend_events')},
                         'wish_events': {'$each': item.get('wish_events')}
                     }
                }, True)

        elif isinstance(item, EventItem):
            self.db[item.collection].update({'id': item.get('id')}, {'$set': item}, True)

        elif isinstance(item, EventUsersItem):
            self.db[item.collection].update(
                {'id': item.get('id')},
                {'$addToSet':
                    {
                        'participants': {'$each': item.get('participants')},
                        'wishers': {'$each': item['wishers']}
                    }
                }, True)

        return item
