# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
import json
from douban_one.transCookie import TransCookie

class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36",
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        ]

    def process_request(self, request, spider):
        request.headers["User-Agent"] = random.choice(self.user_agents)


class CookiesMiddleware(object):
    def __init__(self):
        self.raw_cookies = 'bid=J_g_SHisX78; gr_user_id=beca6b2e-aa82-43d1-a604-88ff981fb1fa; _vwo_uuid_v2=D579AB209A0C8877B86CF14815FD1A626|8b6f4f48aee397f9307f9a7603eb1afa; __gads=ID=03ec97cba11330e4:T=1583660476:S=ALNI_MY8DikdGOLo0lz3Xc60FagnPE-cnQ; viewed="34876107"; __yadk_uid=RcVKq3vxQAl85HHBZk3fTir9KZXNF7aE; douban-fav-remind=1; push_doumail_num=0; __utmv=30149280.21314; loc-last-index-location-id="118281"; ll="118281"; __utmc=30149280; douban-profile-remind=1; ps=y; push_noty_num=0; ct=y; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1587914787%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DczcPQTENhjb_vF4-FBgnlRhB8-h3w01I4GrLut1XSIHAQt914jIinuwIFzm0QVx6%26wd%3D%26eqid%3Dc1a56c5e0000c0c6000000065ea4fa33%22%5D; _pk_ses.100001.8cb4=*; dbcl2="213143591:sjYZotGXf2o"; ck=J-0V; __utma=30149280.553600158.1583660471.1587895023.1587914797.8; __utmz=30149280.1587914797.8.5.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/passport/login; ap_v=0,6.0; _pk_id.100001.8cb4=1b76ec73d67dacec.1583660467.8.1587916467.1587898347.; __utmt=1; __utmb=30149280.8.10.1587914797'
        tc = TransCookie()
        self.cookies = tc.stringToDict(self.raw_cookies)


    def process_request(self, request, spider):
        if self.cookies:
            request.cookies = self.cookies
            print("使用cookies")
        else:
            print("未使用cookies")


if __name__ == "__main__":
    cookieMiddleware = CookiesMiddleware()
    print(type(cookieMiddleware.cookies))
    print(cookieMiddleware.cookies)