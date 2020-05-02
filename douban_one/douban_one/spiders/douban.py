# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from douban_one.items import DoubanUserItem, UserRelationItem, UserEventsItem, EventItem, EventUsersItem
class DoubanSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    start_urls = ['http://douban.com/']
    user_url = "https://www.douban.com/people/{uid}/"
    follow_url = "https://www.douban.com/people/{uid}/contacts?start={start}"
    fan_url = "https://www.douban.com/people/{uid}/rev_contacts?start={start}"
    user_attend_events_url = "https://www.douban.com/location/people/{uid}/events/attend/expired?start={start}"
    user_wish_events_url = "https://www.douban.com/location/people/{uid}/events/wish/expired?start={start}"
    event_url = "https://www.douban.com/event/{eid}/"
    participant_url = "https://www.douban.com/event/{eid}/participant?start={start}"
    wisher_url = "https://www.douban.com/event/{eid}/wisher?start={start}"
    #start_users = ["71563921"] #蚂蚁
    start_users = ["chen__teng"]
    count = 0

    def start_requests(self):
        for uid in self.start_users:
            yield Request(url = self.user_url.format(uid = uid), callback = self.parse_user)


    def parse_user(self, response):
        """
        处理用户信息，并请求用户粉丝和用户关注
        """
        if self.count == 5000:
            print(self.count,"停止")
            self.crawler.engine.close_spider(self, '5000 job done!')
        self.count+=1

        user_name = response.xpath('//div[@class="info"]/h1/text()').extract_first()
        signature = response.xpath('//div[@class="signature_display pl"]/text()').extract_first(default="")
        bd = response.xpath('//div[@class="bd"]')
        id = bd.xpath('.//div[@class="pl"]/text()').extract_first()
        city = bd.xpath('.//div[@class="user-info"]/a/text()').extract_first(default="未知")
        verified_type = bd.xpath('.//div[@class="tooltipped profile-verify-wrapper"]/a/span/text()').extract_first(default="")
        verified = bool(verified_type)
        description = bd.xpath('.//span[@id="intro_display"]/text()').extract()

        user = DoubanUserItem()
        user['id'] = id.strip()
        user['signature'] = signature.strip()
        user['name'] = user_name.strip()
        user['city'] = city.strip()
        user['verified_type'] = verified_type.strip()
        user['verified'] = verified
        user['description'] = " ".join(description) if description else "无"
        print(user)
        userItem = user
        yield userItem
        print("=====================粉丝======================")
        yield Request(self.fan_url.format(uid=user['id'], start=0),
                      callback=self.parse_fans,
                      meta={'uid':user['id'], 'start':0})
        print("=====================关注======================")
        yield Request(self.follow_url.format(uid=user['id'], start=0),
                      callback=self.parse_follows,
                      meta={'uid': user['id'], 'start': 0})
        print("=====================参加事件======================")
        yield Request(self.user_attend_events_url.format(uid=user['id'], start=0),
                      callback=self.parse_user_attend_events,
                      meta={'uid' : user['id'], 'start' : 0})
        print("=====================感兴趣事件======================")
        yield Request(self.user_wish_events_url.format(uid=user['id'], start=0),
                      callback=self.parse_user_wish_events,
                      meta={'uid': user['id'], 'start': 0})

    def parse_user_attend_events(self, response):
        """
        获取当前用户参加过的所有事件，并且爬取参加过的事件的详情
        """
        uid = response.meta.get('uid')

        events_url = response.xpath('//div[@class="title"]/a/@href').extract()
        events_id = []
        for event_url in events_url:
            event_id = event_url.split('/')[-2]
            events_id.append(event_id)
            yield Request(self.event_url.format(eid = event_id),
                          callback=self.parse_event,
                          meta={'eid':event_id})

        events = UserEventsItem()
        events['id'] = uid
        events['attend_events'] = events_id
        events['wish_events'] = []
        userEventsItem = events
        yield userEventsItem

        next = response.xpath('//span[@class="next"]/a').extract()
        if next:
            print(next)
            start = response.meta.get('start')
            start = start + 10
            yield Request(self.user_attend_events_url.format(uid=uid, start=start),
                          callback=self.parse_user_attend_events,
                          meta={'uid': uid, 'start': start})



    def parse_user_wish_events(self, response):
        """
            获取当前用户感兴趣的所有事件，并且爬取参加过的事件的详情（跟处理 用户参加事件 基本相同）
        """
        uid = response.meta.get('uid')
        events_url = response.xpath('//div[@class="title"]/a/@href').extract()
        events_id = []
        for event_url in events_url:
            event_id = event_url.split('/')[-2]
            events_id.append(event_id)
            yield Request(self.event_url.format(eid = event_id),
                          callback=self.parse_event,
                          meta={'eid':event_id})

        events = UserEventsItem()
        events['id'] = uid
        events['attend_events'] = []
        events['wish_events'] = events_id
        userEventsItem = events
        yield userEventsItem

        next = response.xpath('//span[@class="next"]/a').extract()
        if next:
            print(next)
            start = response.meta.get('start')
            start = start + 10
            yield Request(self.user_wish_events_url.format(uid=uid, start=start),
                          callback=self.parse_user_wish_events,
                          meta={'uid': uid, 'start': start})

    def parse_fans(self, response):
        """
            处理用户粉丝， 如果有下一页，处理下一页粉丝
        """

        uid = response.meta.get('uid')            #request转递给response
        fans_url = response.xpath('//a[@class="nbg"]/@href').extract()
        fans_id = []
        for fan_url in fans_url:
            fan_id = fan_url.split('/')[-2]
            fans_id.append(fan_id)
            yield Request(url = self.user_url.format(uid = fan_id), callback = self.parse_user)

        relation = UserRelationItem()
        relation['id'] = uid
        relation['fans'] = fans_id
        relation['follows'] = []
        relationItem = relation
        print(fans_id)
        yield relationItem

        #是否有下一页
        next = response.xpath('//span[@class="next"]/a').extract()
        if next:
            start = response.meta.get('start')
            start = start + 70
            yield Request(self.fan_url.format(uid=uid, start=start),
                          callback=self.parse_fans,
                          meta={'uid':uid, 'start':start})

    def parse_follows(self, response):
        """
            处理用户关注， 如果有下一页，处理下一页关注
        """
        uid = response.meta.get('uid')  # request转递给response
        follows_url = response.xpath('//a[@class="nbg"]/@href').extract()        #跟fans处理相同
        follows_id = []
        for follow_url in follows_url:
            follow_id = follow_url.split('/')[-2]
            follows_id.append(follow_id)
            yield Request(url=self.user_url.format(uid=follow_id), callback=self.parse_user)

        relation = UserRelationItem()
        relation['id'] = uid
        relation['fans'] = []
        relation['follows'] = follows_id
        relationItem = relation
        print(follows_id)
        yield relationItem

        #是否有下一页
        next = response.xpath('//span[@class="next"]/a').extract()
        if next:
            start = response.meta.get('start')
            start = start + 70
            yield Request(self.follow_url.format(uid=uid, start=start),
                          callback=self.parse_follows,
                          meta={'uid':uid, 'start':start})

    def parse_event(self, response):
        """
            获取事件的标题、时间、地点等信息，然后爬取该事件参加者和感兴趣者
        """
        eid = response.meta.get('eid')
        event_info = response.xpath('//div[@class="event-info"]')
        title = event_info.xpath('./h1/text()').extract_first("无")
        date = event_info.xpath('.//li[@class="calendar-str-item"]/text()').extract_first("无")
        location = event_info.xpath('.//div[@itemprop="location"]/span[@itemprop="address"]/span/text()').extract()
        type = event_info.xpath('.//a[@itemprop="eventType"]/text()').extract_first("无")

        event = EventItem()
        event['id'] = eid.strip()
        event['title'] = title.strip()
        event['date'] = date.strip()
        event['location'] = " ".join([l.strip() for l in location]) if location else "无"
        event['type'] = type.strip()
        eventItem = event
        yield eventItem
        yield Request(self.participant_url.format(eid = event['id'], start = 0),
                      callback=self.parse_event_participants,
                      meta={'eid':eid, 'start': 0})
        yield Request(self.wisher_url.format(eid=event['id'], start=0),
                      callback=self.parse_event_wishers,
                      meta={'eid': eid, 'start': 0})

    def parse_event_participants(self, response):
        """
            获取该事件的参加者，如果有下一页，处理下一页参加者
        """
        eid = response.meta.get('eid')
        participants_url = response.xpath('//a[@class="nbg"]/@href').extract()  # 跟fans、follows处理相同
        participants_id = []
        for participant_url in participants_url:
            participant_id = participant_url.split('/')[-2]
            participants_id.append(participant_id)

        eventUsers = EventUsersItem()
        eventUsers['id'] = eid
        eventUsers['participants'] = participants_id
        eventUsers['wishers'] = []
        eventUsersItem = eventUsers
        yield eventUsersItem
        print('参加者')

        #是否有下一页
        next = response.xpath('//span[@class="next"]/a').extract()
        if next:
            start = response.meta.get('start')
            start = start + 70
            yield Request(self.participant_url.format(eid=eid, start=start),
                          callback=self.parse_event_participants,
                          meta={'eid':eid, 'start':start})


    def parse_event_wishers(self, response):
        """
            获取该事件的感兴趣者， 如果有下一页，处理下一页感兴趣者
        """
        eid = response.meta.get('eid')
        wishers_url = response.xpath('//a[@class="nbg"]/@href').extract()  # 跟fans、follows处理相同
        wishers_id = []
        for wisher_url in wishers_url:
            wisher_id = wisher_url.split('/')[-2]
            wishers_id.append(wisher_id)

        eventUsers = EventUsersItem()
        eventUsers['id'] = eid
        eventUsers['participants'] = []
        eventUsers['wishers'] = wishers_id
        eventUsersItem = eventUsers
        yield eventUsersItem
        print('感兴趣者')

        #是否有下一页
        next = response.xpath('//span[@class="next"]/a').extract()
        if next:
            start = response.meta.get('start')
            start = start + 70
            yield Request(self.wisher_url.format(eid=eid, start=start),
                          callback=self.parse_event_wishers,
                          meta={'eid':eid, 'start':start})



