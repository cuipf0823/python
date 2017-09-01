# !/usr/bin/python
# coding=utf-8
from collections import OrderedDict
from .query import *


class Operations:
    # send message without params
    OPT_LIST_SERVER = 'list'
    OPT_ONLINES_SERVER = 'list_onlines'
    OPT_REGISTER_NUM = 'reg_num'
    OPT_TUNNEL_INFO = 'tunnel'

    operations_desc = OrderedDict()
    operations_desc[OPT_LIST_SERVER] = ('查询全部有效服务器', list_server)
    operations_desc[OPT_ONLINES_SERVER] = ('查询全部online信息', online_status)
    operations_desc[OPT_REGISTER_NUM] = ('查询注册人数', register_num)
    operations_desc[OPT_TUNNEL_INFO] = ('查询tunnel信息', tunnel)

    @classmethod
    def operations(cls):
        return cls.operations_desc

    @classmethod
    def callback(cls, opt, **kwargs):
        opt_info = cls.operations_desc.get(opt, None)
        if opt_info is None:
            return None
        return opt_info[1](**kwargs)









