from functools import wraps
import cProfile
import pstats
import io
import time


# decorator示例
# decorator最经典的示例, 给函数调用做缓存
def memo(func):
    cache = {}
    miss = object()

    @wraps(func)
    def wrapper(*args):
        result = cache.get(args, miss)
        if result is miss:
            result = func(*args)
            cache[args] = result
            print(cache)
        return result
    return wrapper


@memo
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)


# profiler示例
def profiler(func):
    def wrapper(*args, **kwargs):
        datafn = func.__name__ + ".profile"
        prof = cProfile.Profile()
        retval = prof.runcall(func, *args, **kwargs)
        prof.dump_stats(datafn)
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(prof, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval
    return wrapper


# 注册回调函数
# 如通过url的路由来调用相关注册的函数示例
class AppRouter:
    def __init__(self):
        self.func_map = {}

    def register(self, name):
        def func_wrapper(func):
            self.func_map[name] = func
            return func
        return func_wrapper

    def call_method(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("No function registered against - " + str(name))
        return func()

app = AppRouter()


@app.register('/')
def main_page_func():
    return "This is the main page."


@app.register('/next_page')
def next_page_func():
    return "This is the next page."


# 给函数打印日志
def logger(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        ts = time.time()
        result = fn(*args, **kwargs)
        te = time.time()
        print("function      = {0}".format(fn.__name__))
        print("    arguments = {0} {1}".format(args, kwargs))
        print("    return    = {0}".format(result))
        print("    time      = %.6f sec" % (te-ts))
        return result
    return wrapper


@logger
def multipy(x, y):
    return x * y


@logger
def sum_num(n):
    s = 0
    for i in range(n+1):
        s += i
    return s


if __name__ == '__main__':
    # print(fib(60))
    print(app.call_method('/'))
    print(app.call_method('/next_page'))
    print(multipy(2, 10))
    print(sum_num(100))
    print(sum_num(10000000))
    pass
