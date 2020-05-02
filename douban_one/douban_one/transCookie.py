# -*- coding: utf-8 -*-

class TransCookie:
    def __init__(self, filename = None):
        self.filename = filename

    def stringToDict(self,cookie):
        '''
        将从浏览器上Copy来的cookie字符串转化为Scrapy能使用的Dict
        :return:
        '''
        itemDict = {}
        items = cookie.split(';')
        for item in items:
            key = item.split('=')[0].replace(' ', '')
            value = item.split('=')[1]
            itemDict[key] = value
        return itemDict

    def getCookieFromFile(self):
        with open(self.filename,'r') as f:
            string_cookie = f.read()
        return self.stringToDict(string_cookie)

if __name__ == "__main__":
    cookie = 'read_mode=day; default_font=font2; locale=zh-CN; Hm_lvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1536841932,1536891052,1536894450,1536895275; remember_user_token=W1sxNDAyNzQ2N10sIiQyYSQxMSRYQUQ2aGcvLkxDRjRWQy5Valhzc0l1IiwiMTUzNjg5NTQ3MC44NzMyMTc2Il0%3D--303a6f7be884ffe65ae2ef21a85a1d43c6daf7ab; _m7e_session=92baba2bd71c62a5eedda75ff55041da; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2214027467%22%2C%22%24device_id%22%3A%22165c23ce89f148-08175020a889ab-5701631-1327104-165c23ce8a06da%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.baidu.com%2Flink%22%2C%22%24latest_referrer_host%22%3A%22www.baidu.com%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_utm_source%22%3A%22desktop%22%2C%22%24latest_utm_medium%22%3A%22index-users%22%7D%2C%22first_id%22%3A%22165c23ce89f148-08175020a889ab-5701631-1327104-165c23ce8a06da%22%7D; Hm_lpvt_0c0e9d9b1e7d617b3e6842e85b9fb068=1536895486'
    trans = TransCookie(cookie)
    print(trans.stringToDict())