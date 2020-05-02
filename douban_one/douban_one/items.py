# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class DoubanUserItem(scrapy.Item):
    """豆瓣用户基本信息"""
    collection = "users"
    id = Field()
    name = Field()
    city = Field()
    verified = Field()
    verified_type = Field()
    signature = Field()
    description = Field()
    follows = Field()
    follows_count = Field()
    fans = Field()
    fans_count = Field()
    attend_events = Field()
    def __str__(self):
        return "{id}\n{name}\n{city}\n{verified_type}\n{signature}\n{description}\n".format(
            id = self['id'],
            name = self['name'],
            city = self['city'],
            verified_type = self['verified_type'],
            signature = self['signature'],
            description = self['description']
        )

class UserRelationItem(scrapy.Item):
    """用户的关系"""
    collection = "users"
    id = Field()
    follows = Field()
    fans = Field()

class UserEventsItem(scrapy.Item):
    """用户参加、感兴趣的事件"""
    collection = "users"
    id = Field()
    attend_events = Field()
    wish_events = Field()

class EventItem(scrapy.Item):
    """事件的基本信息"""
    collection = "events"
    id = Field()
    title = Field()
    date = Field()
    location = Field()
    type = Field()
    attend_users = Field()
    wish_users = Field()

class EventUsersItem(scrapy.Item):
    """事件的参加者、感兴趣者"""
    collection = "events"
    id = Field()
    participants = Field()
    wishers = Field()

