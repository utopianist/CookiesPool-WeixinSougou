import re
import time
import requests
from cookiespool.db import RedisClient
from cookiespool.config import *

headers = {
    'Host': 'weixin.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://weixin.sogou.com/',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
}
url = 'https://weixin.sogou.com/weixin?type=2&query=nba&s_from=input&_sug_=n&_sug_type_=&w=01019900&sut=5296&sst0=1543167134916&lkt=10%2C1543167129476%2C1543167134813'

class Spider():
    def __init__(self):
        self.redis = RedisClient()

    def getHTML(self):
        proxy = self.redis.random()
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            r = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies, timeout=30)
            print('正在使用：', proxy)
            if r.status_code == 200:
                header = r.headers
                print(header)
                snuid = re.findall('(SNUID=.*?;)', header['Set-Cookie'])
                print(snuid)
                if len(snuid) != 0:
                    self.redis.push(snuid[0])
                    print('Redis插入:', snuid[0])
                    while snuid != None:
                        self.circle(proxy)
                        time.sleep(SLEEPTIME)
                    else :
                        self.redis.decrease(proxy)
                else:
                    self.redis.decrease(proxy)
        except TimeoutError:
            pass


    def circle(self, proxy):
        proxies = {
            'http': 'http://' + proxy,
            'https': 'https://' + proxy,
        }
        try:
            r = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
            print('循环代理：', proxy)
            if r.status_code == 200:
                header = r.headers
                print(header)
                snuid = re.findall('(SNUID=.*?;)', header['Set-Cookie'])
                if len(snuid) != 0:
                    self.redis.push(snuid[0])
                    print('Redis插入:', snuid[0])
                    return snuid
                else:
                    snuid = None
                    return snuid
        except:
            snuid = None
            return snuid