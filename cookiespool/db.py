import redis
from cookiespool.config import *
from random import choice
from cookiespool.error import PoolEmptyError


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        """
        初始化
        :param host: Redis 地址
        :param port: Redis 端口
        :param password: Redis密码
        """
        self.db = redis.StrictRedis(host=host, port=port, password=password, decode_responses=True)

    def push(self, snuid):
        """
        从列表头部插入snuid，
        :param snuid: 参数 snuid
        :return: 添加结果
        """
        self.db.lpush(REDIS_KEY, snuid)

    def pop(self):
        """
        移出并获取列表的最后一个元素， 如果列表没有元素会阻塞列表直到等待超时或发现可弹出元素为止。
        :return: 尾部的snuid
        """
        return self.db.brpop(REDIS_KEY)

    def count(self):
        """
        获取数量
        :return: 数量
        """
        return self.db.llen(REDIS_KEY)

    def random(self):
        """
        随机获取有效代理，首先尝试获取最高分数代理，如果不存在，按照排名获取，否则异常
        :return: 随机代理
        """
        result = self.db.zrangebyscore(PROXY_REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(PROXY_REDIS_KEY, 0, 100)
            if len(result):
                return choice(result)
            else:
                raise PoolEmptyError

    def decrease(self, proxy):
        """
        代理值减一分，小于最小值则删除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score = self.db.zscore(PROXY_REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减1')
            return self.db.zincrby(PROXY_REDIS_KEY, proxy, -1)
        else:
            print('代理', proxy, '当前分数', score, '移除')
            return self.db.zrem(PROXY_REDIS_KEY, proxy)


if __name__ == '__main__':
    conn = RedisClient()
    proxy = conn.random()
    print(proxy)
    print(type(proxy))
    decrease = conn.decrease('193.227.49.82:80')

