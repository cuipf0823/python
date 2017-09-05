# !/usr/bin/python
# coding=utf-8
from collections import OrderedDict
from .query import *


class CallBackType:
    PARAM_NONE = 0
    PARAM_UID_CHANNEL = 1
    PARAM_SERVER_ID = 2


class Operations:
    # send message without params
    OPT_LIST_SERVER = 'list'
    OPT_ONLINES_SERVER = 'list_onlines'
    OPT_REGISTER_NUM = 'reg_num'
    OPT_TUNNEL_INFO = 'tunnel'
    OPT_QUERY_PLAYER = 'query_player'
    OPT_PLAYER_DETAIL = 'player_detail'
    OPT_CRAFT_INFO = 'craft_info'
    OPT_FRIEND_LIST = 'friend_list'
    OPT_BLACK_LIST = 'black_list'
    OPT_PUSH_LIST = 'push_list'
    OPT_KICK_PLAYER = 'kick_player'
    OPT_ALL_PLAYERS = 'all_players'
    OPT_ALL_ROOMS = 'all_rooms'

    operations_desc = OrderedDict()
    operations_rsps = OrderedDict()
    operations_desc[OPT_LIST_SERVER] = ('查询全部有效服务器', list_server, CallBackType.PARAM_NONE)
    operations_desc[OPT_ONLINES_SERVER] = ('查询全部online信息', online_status, CallBackType.PARAM_NONE)
    operations_desc[OPT_REGISTER_NUM] = ('查询注册人数', register_num, CallBackType.PARAM_NONE)
    operations_desc[OPT_TUNNEL_INFO] = ('查询tunnel信息', tunnel, CallBackType.PARAM_NONE)

    operations_desc[OPT_QUERY_PLAYER] = ('查询玩家所在服务器', query_player, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_PLAYER_DETAIL] = ('查询玩家详细信息', player_detail, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_CRAFT_INFO] = ('查询玩家星球信息', craft_info, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_FRIEND_LIST] = ('查询玩家好友列表', friend_list, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_BLACK_LIST] = ('查询玩家黑名单列表', black_list, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_PUSH_LIST] = ('查询玩家推送列表', push_list, CallBackType.PARAM_UID_CHANNEL)
    operations_desc[OPT_KICK_PLAYER] = ('强制玩家下线', kick_player, CallBackType.PARAM_UID_CHANNEL)

    operations_desc[OPT_ALL_PLAYERS] = ('查询所有在线用户', query_user_info, CallBackType.PARAM_SERVER_ID)
    operations_desc[OPT_ALL_ROOMS] = ('查询当前所有房间', all_room, CallBackType.PARAM_SERVER_ID)

    operations_rsps[OPT_LIST_SERVER] = handle_list_server

    @classmethod
    def operations(cls):
        return cls.operations_desc

    @classmethod
    def callback(cls, opt, **kwargs):
        opt_info = cls.operations_desc.get(opt, None)
        if opt_info is None:
            return None
        return opt_info[1](**kwargs)

    @classmethod
    def rsp_callback(cls, opt, rsp):
        cb = cls.operations_rsps.get(opt, None)
        if cb is None:
            return None
        return cb(rsp)






