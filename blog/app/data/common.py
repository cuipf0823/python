# !/usr/bin/python
# coding=utf-8
from . import config
from . import color_cmd


gateway_session = 0
# 登陆成功之后服务器返回
gid = 0
# 登陆GM服务的用户名 密码
login_name = ''
login_pwd = ''

# 是否打印到文件中
output = False

# 程序是否初始化完成
is_init = False

# 当前服务器全部online列表
# online_ids
servers_list = []


def write_log(context):
    """
    context打印到文件，用于结果输出到文件
    :param context: 需要打印的内容
    :return:
    """
    pf = None
    try:
        pf = open(config.gm_output_path(), 'ab')
    except IOError as err:
        color_cmd.printred('open file %s failed %s!\n' % (config.gm_output_path(), err))
    if pf:
        pf.write(context)
    pf.close()



