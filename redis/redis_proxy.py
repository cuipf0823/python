# !/usr/bin/python
# coding=utf-8

import redis
import time
r = redis.Redis(host='192.168.208.129', port=6379, db=0)


# 字符串类型
def demo_string():
    r.set('name', 'jack')
    r.set('email', 'jackjack@yahoo.com')
    print r.get('name')
    print r.get('email')
    r.incr('age')
    r.incr('age', 20)
    print r.get('age')
    r.decr('age', 5)
    print r.get('age')
    print r.strlen('name')

    r.mset({'key1': 'v1', 'key2': 'v2'})
    print r.mget(['key1', 'key2'])


# 散列表
def demo_hash_table():
    num = 12
    key = "post:%d" % num
    r.hset(key, 'title', 'hello world')
    r.hset(key, 'author', 'jack')
    r.hset(key, 'time', '2016-12-16')
    r.hset(key, 'content', 'test')
    print r.hgetall(key)


# transaction事务
def demo_transaction():
    r.set('file', 'test.cc')
    with r.pipeline() as pipe:
        while True:
            try:
                # 先关注一个key
                pipe.watch('file')
                pipe.multi()
                pipe.set('file', 'test1.cc')
                pipe.execute()
                break
            except WatchError:
                continue
    print r.get('file')


# 生存时间 限时优惠 缓存 验证码等 多了一点时间就会删除这些数据 redis中可以使用expire实现
# persist set get命令都可以消除键的生存时间
def demo_expire():
    r.set('code', '123456')
    ret = r.expire('code', 6)
    if ret:
        print 'expire set success'
    else:
        return False
    while True:
        if r.exists('code'):
            print r.get('code')
            print r.ttl('code')
        else:
            print 'code timeout del it'
            break
        time.sleep(1)


if __name__ == '__main__':
    demo_string()
    demo_hash_table()
    demo_transaction()
    demo_expire()
