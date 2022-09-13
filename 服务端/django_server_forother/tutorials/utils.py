#!/usr/bin/env python
# coding=utf-8
import redis

from tutorials.config import REDIS_HOST, REDIS_PORT, REDIS_DB_NUM, REDIS_PASSWORD


def get_redis_conn():
    """
    获取redis链接
    :return: redis连接对象
    """
    pool = redis.ConnectionPool(
        host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB_NUM, decode_responses=True)
    redis_conn = redis.Redis(connection_pool=pool)
    return redis_conn


redis_conn = get_redis_conn()

redis_conn.set('foo', 'this is test')
print(redis_conn.get('foo'))
