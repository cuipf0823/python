# !/usr/bin/python
# coding=utf-8

import time
from .proto import gm_pb2 as pb_gm
from . import proto_codec as codec
from . import color_cmd as cmd
from google.protobuf import text_format
from .proto import error_code_pb2 as pb_error
from . import common
from . import handle_cmd

# timer触发的时间间隔
interval = 1
current = time.time()


class HandleMsg(object):
    """
    服务端回复消息的处理
    """
    def __register(self):
        self.__rsp_map = {
            pb_gm._GMCHECKSESSIONRSP.full_name: self.check_session,
            pb_gm._GMLOGINRSP.full_name: self.login,
            pb_gm._GMQUERYONLINEUSERINFORSP.full_name: self.detail,
            pb_gm._GMGETTUNNELSERVERINFORSP.full_name: self.tunnel,
            pb_gm._GMGETALLSERVERLISTRSP.full_name: self.list,
            pb_gm._GMKICKEDRSP.full_name: self.kick,
            pb_gm._GMPUSHMESSAGERSP.full_name: self.push,
            pb_gm._GMQUERYALLUSERBASEINFOONLINERSP.full_name: self.all_user,
            pb_gm._GMGETALLSERVERROOMRSP.full_name: self.rooms
        }

    def __init__(self, parse):
        self.__rsp_map = {}
        self.__parse = parse
        self.__register()

    @staticmethod
    def callback(func, *args):
        func(*args)

    def timer(self):
        # 保证1s左右触发一次
        global interval
        global current
        now = time.time()
        if now >= interval + current:
            self.__parse.timer()
            current = time.time()

    @staticmethod
    def check_session(header, rsp):
        # 设置gateway_session
        common.gateway_session = header.gateway_session
        handle_cmd.login_req(common.login_name, common.login_pwd, rsp.random_bytes)

    def login(self, header, rsp):
        if rsp.HasField('gid'):
            common.gid = rsp.gid
        print(common.gid)
        cmd.printgreen('Login GM Server successfully! \n')
        handle_cmd.list_server()
        pass

    def detail(self, header, rsp):
        if len(str(rsp)) == 0:
            cmd.printred('Input user offline or uid invalid currently !\n')
        else:
            cmd.printyellow(str(text_format.MessageToString(rsp)))

    def kick(self, header, rsp):
        if len(str(rsp)) == 0:
            cmd.printgreen('Input user kick offline or uid invalid currently \n')
        else:
            cmd.printgreen('Kick User info Response, Kick result check by "detail": \n')
            cmd.printyellow(str(text_format.MessageToString(rsp)))

    def tunnel(self, header, rsp):
        if len(str(rsp)) == 0:
            cmd.printgreen('GM Server response empty, Currently tunnel server empty \n')
        else:
            cmd.printgreen('Tunnel Server Info:\n')
            cmd.printyellow(str(text_format.MessageToString(rsp)))
            cmd.printyellow('Current Tunnel Servers: %u \n' % len(rsp.servers))

    def list(self, header, rsp):
        if common.is_init:
            if len(str(rsp)) == 0:
                cmd.printgreen('GM Server response empty, Gateway and Online server not exist\n')
            else:
                cmd.printgreen('Gateway or Online Server info: \n')
                rsp_str = str(text_format.MessageToString(rsp)).replace('server_type: 1','server_type: Gateway')
                cmd.printyellow(rsp_str.replace('server_type: 2','server_type: Online'))
        else:
            for item in rsp.server_items:
                if item.server_type == 2:
                    common.servers_list.append(item.zone_id)
            # 初始化完成
            common.is_init = True
            self.__parse.help()

    @staticmethod
    def all_user(header, rsp):
        cmd.printyellow(str(text_format.MessageToString(rsp)))
        cmd.printyellow('Current Server Online player: %u \n' % len(rsp.players))
        pass

    @staticmethod
    def rooms(header, rsp):
        cmd.printyellow(str(text_format.MessageToString(rsp)))
        cmd.printyellow('Current Server rooms count: %u \n' % len(rsp.room_ids))

    def push(self, header, rsp):
        if len(str(rsp)) == 0:
            cmd.printgreen('Push Message to all users Successfully !\n')

    def msg_dispather(self, data):
        if data:
            header, body = codec.BaseCodec.decode(data)
            msg_name = header.msg_name.decode()
            if header.errcode is 0:
                if msg_name in self.__rsp_map.keys():
                    HandleMsg.callback(self.__rsp_map[msg_name], header, body)
                else:
                    if len(str(body)) == 0:
                        cmd.printred('GM Server response empty \n')
                    cmd.printgreen('GM Server Response:\n')
                    cmd.printyellow(str(text_format.MessageToString(body)))
                if common.output:
                    common.write_log('GM Server response: \n' + str(text_format.MessageToString(body)))
            else:
                cmd.printred('error code: %d %s \n' % (header.errcode, pb_error.GMErrorCode.Name(header.errcode)))
                if common.output:
                    common.write_log('GM Server response: \n error code: %d %s \n' %
                                           (header.errcode, pb_error.GMErrorCode.Name(header.errcode)))
        return

