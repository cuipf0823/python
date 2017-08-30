#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from collections import OrderedDict
from . import color_cmd as cmd
from . import handle_cmd
from . import common
from . import config
from . import mail


class CmdParse(object):
    """
    CmdParse用于处理用户的输入命令
    """
    def __init__(self):
        self.__cmds = OrderedDict()
        self.register_cmd()
        self.__timer_cmds = OrderedDict()
        self.register_timer_cmd()
        self.__queue = []
        self.__exec_flag = False
        pass

    def register_cmd(self):
        self.__cmds['help'] = (self.help, 'display help information')
        self.__cmds['quit'] = (self.quit, 'quit gm client')
        self.__cmds['login'] = (self.login, 'login gm server')
        self.__cmds['kick'] = (self.kick_user, 'kick user offline')
        self.__cmds['tunnel'] = (handle_cmd.tunnel, 'get tunnel infomation')
        self.__cmds['list'] = (handle_cmd.list_server, 'list all gateway or online server information')
        self.__cmds['detail'] = (self.user_detail, 'get online user detail information')
        self.__cmds['query_user'] = (self.query_user, 'query which online server user belong to')
        self.__cmds['query_online'] = (self.query_online, 'query user online or offline')
        self.__cmds['reg_num'] = (self.register_num, 'get online server register num')
        self.__cmds['online_status'] = (self.online_status, 'get online server status')
        self.__cmds['all_user'] = (self.query_user_info, 'get all user info in online server')
        self.__cmds['push'] = (self.push, 'push message to all online users')
        self.__cmds['mode'] = (self.mode, 'set result output mode')
        self.__cmds['timer'] = (self.cmd_timer, 'execute the command regularly')
        self.__cmds['kill'] = (self.kill, 'kill all timed task')
        self.__cmds['rooms'] = (self.all_room, 'get server all rooms id')
        self.__cmds['room_info'] = (self.room_info, 'get one room detail information')
        self.__cmds['crafts'] = (self.craft_info, 'get player all crafts information')
        self.__cmds['friends'] = (self.friend_list, 'get player all friends')
        self.__cmds['blacks'] = (self.black_list, 'get player black list')
        self.__cmds['push_list'] = (self.push_list, 'get player push list')
        self.__cmds['get_mail'] = (self.get_unsend_mail, 'get unsend mail')
        self.__cmds['del_mail'] = (self.del_unsend_mail, 'delete unsend mail')
        self.__cmds['send_mail'] = (self.send_mail, 'send mail')

    def register_timer_cmd(self):
        """
        timer_cmd格式说明：key为cmd，value=（flag，interval，times）
        :return:
        """
        self.__timer_cmds['tunnel'] = handle_cmd.tunnel
        self.__timer_cmds['list'] = handle_cmd.list_server
        self.__timer_cmds['reg_num'] = handle_cmd.register_num
        self.__timer_cmds['online_status'] = handle_cmd.online_status

    @staticmethod
    def callback(func):
        func()

    @staticmethod
    def quit():
        cmd.printgreen('GM Client quit ...\n')
        pass

    def help(self):
        """
        print cmd info
        """
        cmd.printgreen('You obtain information by using commands below:\n')
        num = 0
        for key, value in self.__cmds.items():
            num += 1
            cmd.printgreen('%-2d. %-15s%s \n' % (num, key, value[-1]))

    def valid(self, str_cmd):
        return str_cmd in self.__cmds.keys()

    def parse(self, str_cmd):
        if common.output:
            common.write_log('Commmand: ' + str_cmd + '\n')
        CmdParse.callback(self.__cmds[str_cmd][0])

    def timer(self):
        if not self.__exec_flag:
            return
        if len(self.__queue) == 0:
            self.__exec_flag = False
            return
        for i, item in enumerate(self.__queue):
            interval = item[1]
            times = item[2]
            left_time = item[3]
            left_times = item[4]
            # 无限次执行
            if times == 0:
                if left_time == 0:
                    str = '\nExecute timed command "%s": \n' % item[0]
                    cmd.printyellow(str)
                    if common.output:
                        common.write_log(str)
                    self.__timer_cmds[item[0]]()
                    item[3] = interval
                else:
                    item[3] = left_time - 1
            else:
                if left_time == 0:
                    if left_times == 0:
                        self.__queue.pop(i)
                    else:
                        str = '\nExecute timed command "%s" times: %d: \n' % (item[0], times - left_times + 1)
                        cmd.printyellow(str)
                        if common.output:
                            common.write_log(str)
                        self.__timer_cmds[item[0]]()
                        item[3] = interval
                        item[4] = left_times - 1
                else:
                    item[3] = left_time - 1

    @staticmethod
    def login():
        cmd.printgreen('Login GM Server input login name:\n')
        common.login_name = input().strip('\n')
        cmd.printgreen('Login GM Server input login password:\n')
        common.login_pwd = input().strip('\n')
        handle_cmd.check_session(common.login_name)

    @staticmethod
    def register_num():
        server_id = 0
        while True:
            cmd.printgreen('input server id like ("all or 30000, 30001..."):\n')
            server_str = raw_input().strip('\n')
            if 'all' == server_str:
                break
            if server_str.isdigit() and int(server_str) in common.servers_list:
                server_id = int(server_str)
                break
            else:
                cmd.printred('server id %s invalid Please input again\n' % server_str)
                continue
        handle_cmd.register_num(server_id)

    @staticmethod
    def online_status():
        server_id = 0
        while True:
            cmd.printgreen('input server id like ("all or 30000, 30001..."):\n')
            server_str = raw_input().strip('\n')
            if 'all' == server_str:
                break
            if server_str.isdigit() and int(server_str) in common.servers_list:
                server_id = int(server_str)
                break
            else:
                cmd.printred('server id %s invalid Please input again\n' % server_str)
                continue
        handle_cmd.online_status(server_id)

    @staticmethod
    def query_user():
        uid = 0
        while True:
            cmd.printgreen('query user uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid = int(uid_str)
                break
            else:
                cmd.printred('user uid only include digit please input uid again\n')
        handle_cmd.query_user(uid)

    @staticmethod
    def query_online():
        uid = 0
        while True:
            cmd.printgreen('query user uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid = int(uid_str)
                break
            else:
                cmd.printred('user uid only include digit please input uid again!\n')
        handle_cmd.query_online(uid)

    @staticmethod
    def query_user_info():
        server_id = 0
        while True:
            cmd.printgreen('input server id:\n')
            id_str = raw_input().strip('\n')
            if id_str.isdigit() and int(id_str) in common.servers_list:
                server_id = int(id_str)
                break
            else:
                cmd.printred('server_id not exists please input again!\n')
        handle_cmd.query_user_info(server_id)

    @staticmethod
    def kick_user():
        uid = 0
        while True:
            cmd.printgreen('kick user uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid = int(uid_str)
                break
            else:
                cmd.printred('user uid only include digit please input uid again!\n')
        handle_cmd.kick_user(uid)

    @staticmethod
    def user_detail():
        uid = 0
        while True:
            cmd.printgreen('query user detail info input uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid = int(uid_str)
                break
            else:
                cmd.printred('user uid only include digit please input uid again!\n')
        handle_cmd.user_detail(uid)

    @staticmethod
    def mode():
        common.output = not common.output
        if common.output:
            if os.path.exists(os.path.dirname(config.gm_output_path())):
                cmd.printgreen('Change Output mode, result print to console and file(%s) \n'
                               % config.gm_output_path())
            else:
                cmd.printgreen('Change Output mode failed, directory %s not exists \n' %
                               os.path.dirname(config.gm_output_path()))
                common.output = not common.output
        else:
            cmd.printgreen('Change Output mode, result only print to console \n')

    @staticmethod
    def push():
        server_ids = []
        while True:
            server_ids = []
            cmd.printgreen('Input server id like ("all or 30000, 30001..."):\n')
            server_str = raw_input().strip('\n')
            if server_str == 'all':
                break
            else:
                num_list = server_str.replace(' ', '').split(',')
                for item in num_list:
                    if item.isdigit() and int(item) in common.servers_list:
                        server_ids.append(int(item))
                    else:
                        cmd.printred('server id %s not exists, please input again \n' % item )
                        break
                if len(server_ids) == len(num_list):
                    break
        path = ''
        while True:
            cmd.printgreen('Input read push message file path:\n')
            path = raw_input().strip('\n').rstrip()
            if not os.path.exists(path) or not os.path.isfile(path):
                cmd.printred('file path %s not exists or path not file\n' % path)
                continue
            else:
                break
        fp = None
        try:
            fp = open(path, 'rb')
        except IOError as err:
            cmd.printred('open file %s failed %s' % err)
        context = fp.read()
        fp.close()
        cmd.printgreen('Push Message: \n')
        print(context)
        cmd.printgreen('Are you sure to send ? [yes or no] \n')
        ret = raw_input().strip('\n')
        if ret == 'yes':
            handle_cmd.push(context, server_ids)
        else:
            cmd.printred('Push Message to all users cancel !\n')

    def cmd_timer(self):
        cmd.printgreen('You can execute the below command regularly: \n')
        num = 0
        for key in self.__timer_cmds.keys():
            num += 1
            cmd.printgreen('%-2d. %-15s \n' % (num, key))
        cmd.printgreen('input format cmd -t=interval -c=times or cmd -t=interval \n')
        while True:
            cmd.printgreen('append timed command: \n')
            cmd_str = raw_input().strip('\n').split(' ')
            if len(cmd_str) < 2 or len(cmd_str) > 3:
                cmd.printred('input command format error !\n')
                continue
            if not self.__timer_cmds.has_key(cmd_str[0]):
                cmd.printred('%s command not supported execute regularly \n' % cmd_str[0])
                continue
            if '-t=' not in cmd_str[1] or not cmd_str[1][3:].isdigit():
                cmd.printred('input command format error !\n')
                continue
            if len(cmd_str) == 3:
                if '-c=' not in cmd_str[2] or not cmd_str[2][3:].isdigit():
                    cmd.printred('input command format error !\n')
                    continue
                # [cmd, interval, times, left_time, left_times]
                times = int(cmd_str[2][3:])
                self.__queue.append([cmd_str[0], int(cmd_str[1][3:]), times, 0, times])
            else:
                self.__queue.append([cmd_str[0], int(cmd_str[1][3:]), 0, 0, 0])
            cmd.printgreen('Are you continue append timed command [yes or no]: \n')
            ret = raw_input().strip('\n').lstrip().rstrip()
            if ret == 'yes':
                continue
            else:
                self.__exec_flag = True
                cmd.printgreen('start execute timed command !\n')
                break
        # print(self.__queue)

    def kill(self):
        self.__exec_flag = False
        self.__queue = []
        cmd.printgreen('Kill all timer task successfully !\n')

    @staticmethod
    def all_room():
        server_id = 0
        while True:
            cmd.printgreen('input server id:\n')
            id_str = raw_input().strip('\n')
            if id_str.isdigit() and int(id_str) in common.servers_list:
                server_id = int(id_str)
                break
            else:
                cmd.printred('server not exists please input again!\n')
        handle_cmd.all_room(server_id)
        pass

    @staticmethod
    def room_info():
        server_id = 0
        while True:
            cmd.printgreen('input server id:\n')
            id_str = raw_input().strip('\n')
            if id_str.isdigit() and int(id_str) in common.servers_list:
                server_id = int(id_str)
                break
            else:
                cmd.printred('server id not exists please input again!\n')
        room_id = 0
        while True:
            cmd.printgreen('query room id:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                room_id = int(uid_str)
                break
            else:
                cmd.printred('room id only include digit please input again\n')
        handle_cmd.room_info(server_id, room_id)
        pass

    @staticmethod
    def craft_info():
        uid_id = 0
        while True:
            cmd.printgreen('query player uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid_id = int(uid_str)
                break
            else:
                cmd.printred('uid only include digit please input again\n')
        handle_cmd.craft_info(uid_id)
        pass

    @staticmethod
    def friend_list():
        uid_id = 0
        while True:
            cmd.printgreen('query player uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid_id = int(uid_str)
                break
            else:
                cmd.printred('uid only include digit please input again\n')
        handle_cmd.friend_list(uid_id)
        pass

    @staticmethod
    def black_list():
        uid_id = 0
        while True:
            cmd.printgreen('query player uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid_id = int(uid_str)
                break
            else:
                cmd.printred('uid only include digit please input again\n')
        handle_cmd.black_list(uid_id)
        pass

    @staticmethod
    def push_list():
        uid_id = 0
        while True:
            cmd.printgreen('query player uid:\n')
            uid_str = raw_input().strip('\n')
            if uid_str.isdigit():
                uid_id = int(uid_str)
                break
            else:
                cmd.printred('uid only include digit please input again\n')
        handle_cmd.push_list(uid_id)
        pass

    @staticmethod
    def send_mail():
        ret = mail.check_mail_config()
        print(ret.state)
        if ret.result:
            handle_cmd.send_mail(mail.mail_info)

    @staticmethod
    def get_unsend_mail():
        handle_cmd.unsend_mail()

    @staticmethod
    def del_unsend_mail():
        mail_id = 0
        while True:
            cmd.printgreen('delete unsend mail id:\n')
            uid_str = input().strip('\n')
            if uid_str.isdigit():
                mail_id = int(uid_str)
                break
            else:
                cmd.printred('uid only include digit please input again\n')
        handle_cmd.del_unsend_mail(mail_id)

