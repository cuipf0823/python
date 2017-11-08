# !/usr/bin/python
# coding=utf-8

import redis
import time
import random
from datetime import datetime


r = redis.Redis(host='192.168.154.128', port=6379, db=1, password='123456')
rd = r


# 字符串类型
def demo_string():
    r.set('name', 'jack')
    r.set('email', 'jackjack@yahoo.com')
    print(r.get('name'))
    print(r.get('email'))
    r.incr('age')
    r.incr('age', 20)
    print(r.get('age'))
    r.decr('age', 5)
    print(r.get('age'))
    print(r.strlen('name'))

    r.mset({'key1': 'v1', 'key2': 'v2'})
    print(r.mget(['key1', 'key2']))


# 散列表
def demo_hash_table():
    num = 12
    key = "post:%d" % num
    r.hset(key, 'title', 'hello world')
    r.hset(key, 'author', 'jack')
    r.hset(key, 'time', '2016-12-16')
    r.hset(key, 'content', 'test')
    print(r.hgetall(key))


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
    print(r.get('file'))


# 生存时间 限时优惠 缓存 验证码等 多了一点时间就会删除这些数据 redis中可以使用expire实现
# persist set get命令都可以消除键的生存时间
# expireat 和 expire 区别在于前者使用unix时间作为键的生存时间的截止时间
def demo_expire():
    r.set('code', '123456')
    ret = r.expire('code', 6)
    if ret:
        print('expire set success')
    else:
        return False
    while True:
        if r.exists('code'):
            print(r.get('code'))
            print(r.ttl('code'))
        else:
            print('code timeout del it')
            break
        time.sleep(1)


# 减轻服务器压力，限制单用户一段时间访问量
# 没访问一次增加1 并设置生存时间1分钟即可
def visit(ip):
    key = 'rate.limiting:%s' % ip
    if r.exists(key):
        times = r.incr(key)
        print(times)
        if times > 50:
            print('visit too frequent')
            return False
    else:
        with r.pipeline() as pipe:
            pipe.multi()
            r.incr(key)
            r.expire(key, 30)
            pipe.execute()
    return True


# 限制单用户时间段内访问量算法优化
def optimize_visit(ip):
    lt = 'lrate.limiting:%s' % ip
    length = r.llen(lt)
    if length < 10:
        r.lpush(lt, time.time())
        print(r.l)
    else:
        te = float(r.lindex(lt, 1))
        if time.time() - te < 60:
            print("visit too frequent optimize visit")
            return False
        else:
            r.lpush(lt, time.time())
            r.ltrim(lt, 0, 9)
    return True


def demo_pressure():
    ip = '192.168.208.129'
    # key = 'rate.limiting:%s' % ip
    while True:
        if not visit(ip):
            print('you can not visit')
            break
    while True:
        if optimize_visit(ip):
            print('you can not visit optimize visit')
            break


# 排序sort sort可以对列表类型，集合类型和有序集合类型进行排序
def demo_sort():
    set_name = 'letters'
    set_name1 = 'letters1'
    r.sadd(set_name, 'a', 'k', 'h', 'b', 'd')
    r.sadd(set_name1, 'y', 'k', 'u', 'c', 'd')
    print(r.sdiff(set_name, set_name1))
    print(r.sdiff(set_name1, set_name))
    set_name2 = 'integer'
    r.sadd(set_name2, 100, 2, 3, 9, 10, 89)
    print(r.sort(set_name2))
    print(r.sort(set_name2, None, None, None, None, True))
    # 使用by sort 将lt中元素排序，按照item:*的值进行
    lt = 'sore'
    r.lpush(lt, 1, 2, 3)
    r.set('item:1', 50)
    r.set('item:2', -10)
    r.set('item:3', 100)
    print(r.sort(lt, None, None, 'item:*'))


def insert_data(queue, queue1):
    count = 0
    while True:
        if count >= 10:
            break
        else:
            r.lpush(queue1, random.random())
            r.lpush(queue, random.randint(1, 999))
            count += 1
            time.sleep(1)
    pass


def demo_queue(inst, queue, queue1):
    """
    redis 实现普通的任务队列
    brpop 可以同时检测多个队列，利用这个机制可以实现优先队列，多个键则是从左到右的顺序取出
    """
    while True:
        task = inst.brpop((queue, queue1), 0)
        print(task)
    pass


###################################################################
# redis实际使用
# redis实现用户登录和注册
def register(email, name, pwd):
    """
    这里不再做参数的校验
    键名：user：id
    添加散列类型的键：email.to.id 来保存邮箱和用户ID之间的关系
    """
    user_id = r.incr('users:count')
    # 存储用户信息
    r.hmset('user:%d' % user_id, {'email': email, 'name': name, 'password': pwd})
    r.hset('email.to.id', email, user_id)


# 用户登录验证email和pwd，首先通过email.to.id获取用户ID
def login(email, password):
    user_id = r.hget(email)
    if user_id != 0:
        pwd = r.hget('user:%d' % user_id, 'password')
        if pwd == password:
            print('login successful')
    else:
        print('user not register')


# 修改密码 防止用户频繁访问
def change_pwd(email):
    key_name = 'rate.limiting:%s' % email
    if r.llen(key_name) < 10:
        r.lpush(key_name, time.time())
    else:
        last_time = r.lindex(key_name, -1)
        if time.time() - last_time < 60:
            print('visit too frequently')
            return
        else:
            r.lpush(key_name, time.time())
            r.ltrim(key_name, 0, 9)
    # 发送修改密码连接


# 实现输入自动完成
def init_data():
    ruby = 'ruby'
    re = 'redis'
    r.sadd('prefix:r', ruby, re)
    r.sadd('prefix:ru', ruby)
    r.sadd('prefix:rub', ruby)
    r.sadd('prefix:ruby', ruby)
    r.sadd('prefix:re', re)
    r.sadd('prefix:red', re)
    r.sadd('prefix:redi', re)
    auto = 'autocomplete'
    r.zadd(auto, 'r', 0, 're', 0, 'red', 0, 'redis*', 0, 'ru', 0, 'rub', 0, 'ruby*', 0)


# 自动完成如果要实现的更加完善一点 可以保存每个标签的访问量然后利用sort加by参数排序
def auto_in(prefix):
    key = 'prefix:%s' % prefix
    print(r.smembers(key))


# 使用有序集合完成实现自动输入，zrange取值可以参考标签的平均长度和需要获取标签的数量来决定
# 返回结果遍历即可，区域前缀匹配且结尾是*的
def auto_in1(prefix):
    rank = r.zrank('autocomplete', prefix)
    results = r.zrange('autocomplete', rank + 1, rank + 100)
    print(results)


'''
1. 文章详细信息; 使用redis中的散列类型保存; key是'post:id'; 字段包括: title author time content category;
2. 文章总数; 保存于posts:count中; 只增不减;
3. 文章ID列表; 使用列表类型posts:list记录文章列表;
    a. 新文章发布使用LPUSH将文章加入到列表中;
    b. 删除文章 LREM
    c. 文章分页显示 LRANGE
4. 删除文章列表; 使用列表类型保存 posts:del:list
'''

POSTS_LIST = 'posts:list'
POSTS_COUNT = 'posts:count'
POSTS_DEL_LIST = 'posts:del_list'
# 单页显示文章数
POST_NUM_PAGE = 10


def publish_post(title, author, content, category):
    """
     发布新文章 暂时不加锁 后续添加
    """
    post_id = rd.incr(POSTS_COUNT)
    rd.hmset('post:{}'.format(post_id), {'title': title, 'author': author, 'content': content, 'category': category,
                                         'time': datetime.utcnow()})
    rd.lpush(POSTS_LIST, post_id)


def delete_post(post_id):
    """
    删除文章 需要原子操作 后续修改
    """
    rd.lrem(POSTS_LIST, post_id, 0)
    rd.lpush(POSTS_DEL_LIST, post_id)


def posts_by_page(page_id):
    """
    分页显示
    :param page_id:页码从1开始
    :return:文章ID list key均为bytes
    """
    pages = int(rd.llen(POSTS_LIST) / POST_NUM_PAGE + 1)
    if 0 < page_id <= pages:
        return rd.lrange(POSTS_LIST, (page_id - 1) * POST_NUM_PAGE, page_id * POST_NUM_PAGE - 1)
    else:
        print('invaild param page id[{0}, {1}]'.format(1, pages))
        return None


def get_posts(post_id):
    """
    获取文章信息 返回字典 key value均为bytes
    """
    return rd.hgetall('post:{}'.format(post_id))


def convert(data):
    if isinstance(data, bytes):
        return data.decode('utf-8')
    if isinstance(data, dict):
        return dict(map(convert, data.items()))
    if isinstance(data, tuple):
        return map(convert, data)
    return data


if __name__ == '__main__':
    # demo_string()
    # demo_hash_table()
    # demo_transaction()
    # demo_expire()
    # demo_pressure()
    """
    demo_sort()
    queue_name = 'queue'
    queue_name1 = 'queue1'
    thread = threading.Thread(target=demo_queue, args=(r, queue_name, queue_name1))
    thread.start()
    insert_data(queue_name, queue_name1)
    
    init_data()
    auto_in('r')
    auto_in('re')
    auto_in1('r')
    
    print(convert(get_posts(32)))
    """
    print(get_posts.__doc__)
