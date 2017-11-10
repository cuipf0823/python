# !/usr/bin/python
# coding=utf-8

import redis
import time
import random
import location

rd = redis.Redis(host='192.168.154.128', port=6379, db=1, password='123456')


# 生存时间 限时优惠 缓存 验证码等 多了一点时间就会删除这些数据 redis中可以使用expire实现
# persist set get命令都可以消除键的生存时间
# expireat 和 expire 区别在于前者使用unix时间作为键的生存时间的截止时间
def demo_expire():
    rd.set('code', '123456')
    ret = rd.expire('code', 6)
    if ret:
        print('expire set success')
    else:
        return False
    while True:
        if rd.exists('code'):
            print(rd.get('code'))
            print(rd.ttl('code'))
        else:
            print('code timeout del it')
            break
        time.sleep(1)


# 减轻服务器压力，限制单用户一段时间访问量
# 没访问一次增加1 并设置生存时间1分钟即可
def visit(ip):
    key = 'rate.limiting:%s' % ip
    if rd.exists(key):
        times = rd.incr(key)
        print(times)
        if times > 50:
            print('visit too frequent')
            return False
    else:
        with rd.pipeline() as pipe:
            pipe.multi()
            rd.incr(key)
            rd.expire(key, 30)
            pipe.execute()
    return True


# 限制单用户时间段内访问量算法优化
def optimize_visit(ip):
    lt = 'lrate.limiting:%s' % ip
    length = rd.llen(lt)
    if length < 10:
        rd.lpush(lt, time.time())
        print(rd.l)
    else:
        te = float(rd.lindex(lt, 1))
        if time.time() - te < 60:
            print("visit too frequent optimize visit")
            return False
        else:
            rd.lpush(lt, time.time())
            rd.ltrim(lt, 0, 9)
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
    rd.sadd(set_name, 'a', 'k', 'h', 'b', 'd')
    rd.sadd(set_name1, 'y', 'k', 'u', 'c', 'd')
    print(rd.sdiff(set_name, set_name1))
    print(rd.sdiff(set_name1, set_name))
    set_name2 = 'integer'
    rd.sadd(set_name2, 100, 2, 3, 9, 10, 89)
    print(rd.sort(set_name2))
    print(rd.sort(set_name2, None, None, None, None, True))
    # 使用by sort 将lt中元素排序，按照item:*的值进行
    lt = 'sore'
    rd.lpush(lt, 1, 2, 3)
    rd.set('item:1', 50)
    rd.set('item:2', -10)
    rd.set('item:3', 100)
    print(rd.sort(lt, None, None, 'item:*'))


def insert_data(queue, queue1):
    count = 0
    while True:
        if count >= 10:
            break
        else:
            rd.lpush(queue1, random.random())
            rd.lpush(queue, random.randint(1, 999))
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


def make_html_tag(tag, *args, **kwds):
    def real_decorator(fn):
        css_class = " class='{0}'".format(kwds["css_class"]) if "css_class" in kwds else ""

        def wrapped(*args, **kwds):
            return "<"+tag+css_class+">" + fn(*args, **kwds) + "</"+tag+">"
        return wrapped
    return real_decorator


@make_html_tag(tag="b", css_class="bold_css")
@make_html_tag(tag="i", css_class="italic_css")
def hello():
    return "hello world"

# 输出：
# <b class='bold_css'><i class='italic_css'>hello world</i></b>


if __name__ == '__main__':
    print(hello())
    print(make_html_tag.__name__)
    print(hello.__name__)

    for idx in range(0, 50):
        location.update_contact(rd, 'evan', '{}evan'.format(idx))

    print(location.autocomplete_contact(rd, 'evan', '2'))
    pass
