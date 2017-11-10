# decorator.py
记录一下decorator使用示例
## fib和装饰器memo
fib是斐波那契数列的递归算法, 如果不使用装饰器, 效率非常低, 因为都会重复计算; 比如：我们要计算fib(5)，于是其分解成fib(4) + fib(3)，而fib(4)分解成fib(3)+fib(2)，fib(3)又分解成fib(2)+fib(1)…… 你可看到，基本上来说，fib(3), fib(2), fib(1)在整个递归过程中被调用了两次。

而我们使用了memo装饰器, 在调用函数之前查一下缓存, 缓存中存在就不用计算了, 这样子, 递归从二叉树式递归变成了线性递归;

## AppRouter
演示了通过URL的路由来调用相关注册函数;


# redis/location.py
## 利用redis实现自动补全功能
* 少量数据, 可以使用redis保存, 由python自身实现补全; 效率低;
* 利用redis实现自动补全
