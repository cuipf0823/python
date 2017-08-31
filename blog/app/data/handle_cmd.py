# !/usr/bin/python
#  -*- coding: utf-8 -*-

import hashlib

from blog.app import tcp_con
from . import common
from . import proto_codec as codec
from ..proto import cs_basic_pb2 as pb_basic
from ..proto import gm_pb2 as pb_gm

msg_seq = 0


def encode(header, body):
    return codec.BaseCodec.encode(header, body)


def seq_num():
    global msg_seq
    msg_seq += 1
    return msg_seq


def make_header(msg_name):
    header = pb_basic.CSMessageHeader()
    header.msg_name = msg_name.encode('utf-8')
    header.seq_num = seq_num()
    header.gateway_session = common.gateway_session
    return header


def check_session(name):
    req = pb_gm.GMCheckSessionReq()
    header = make_header(req.DESCRIPTOR.full_name)
    header.gateway_session = 0
    req.name = name.encode('utf-8')
    tcp_con.send(encode(header, req))


def login_req(name, pwd, random_bytes):
    req = pb_gm.GMLoginReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.random_bytes = random_bytes
    md5 = hashlib.md5((name + pwd + random_bytes.decode()).encode('utf-8'))
    req.encrypt_bytes = md5.hexdigest().encode('utf-8')
    tcp_con.send(encode(header, req))


def list_server():
    req = pb_gm.GMGetAllServerListReq()
    header = make_header(req.DESCRIPTOR.full_name)
    tcp_con.send(encode(header, req))


def register_num(server_id=0):
    req = pb_gm.GMGetServerRegisterNumberReq()
    header = make_header(req.DESCRIPTOR.full_name)
    if server_id != 0:
        req.server_ids.append(server_id)
    tcp_con.send(encode(header, req))


def online_status(server_id=0):
    req = pb_gm.GMGetOnlineInSwitchReq()
    header = make_header(req.DESCRIPTOR.full_name)
    if server_id != 0:
        req.server_ids.append(server_id)
    tcp_con.send(encode(header, req))


def query_user(uid, channel=0):
    req = pb_gm.GMQueryUserReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.players.uid = uid
    req.players.channel = channel
    tcp_con.send(encode(header, req))


def query_online(uid, channel=0):
    req = pb_gm.GMQueryUserOnlineReq()
    header = make_header(req.DESCRIPTOR.full_name)
    info = req.players.add()
    info.uid = uid
    info.channel = channel
    tcp_con.send(encode(header, req))


def query_user_info(server_id):
    req = pb_gm.GMQueryAllUserBaseInfoOnlineReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.server_id = server_id
    tcp_con.send(encode(header, req))


def kick_user(uid, channel=0):
    req = pb_gm.GMKickUserReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.uid = uid
    req.channel = channel
    tcp_con.send(encode(header, req))


def user_detail(uid, channel=0):
    req = pb_gm.GMQueryOnlineUserInfoReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.uid = uid
    req.channel = channel
    tcp_con.send(encode(header, req))


def tunnel():
    req = pb_gm.GMGetTunnelServerInfoReq()
    header = make_header(req.DESCRIPTOR.full_name)
    tcp_con.send(encode(header, req))


def push(msg, server_ids):
    req = pb_gm.GMPushMessageReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.push_message = msg
    if len(server_ids) != 0:
        for item in server_ids:
            req.server_ids.append(int(item))
    tcp_con.send(encode(header, req))


def all_room(server_id):
    req = pb_gm.GMGetAllServerRoomReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.server_id = server_id
    tcp_con.send(encode(header, req))


def room_info(server_id, room_id):
    req = pb_gm.GMGetRoomInfoReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.server_id = server_id
    req.room_id = room_id
    tcp_con.send(encode(header, req))


def craft_info(uid, channel=0):
    req = pb_gm.GMGetPlayerCraftInfoReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.uid = uid
    req.channel = channel
    tcp_con.send(encode(header, req))


def friend_list(uid, channel=0):
    req = pb_gm.GMGetFriendListReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.uid = uid
    req.channel = channel
    tcp_con.send(encode(header, req))


def black_list(uid, channel=0):
    req = pb_gm.GMGetBlackListReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.uid = uid
    req.channel = channel
    tcp_con.send(encode(header, req))


def push_list(uid, channel=0):
    req = pb_gm.GMGetPushListReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.uid = uid
    req.channel = channel
    tcp_con.send(encode(header, req))


def send_mail(mail_info):
    req = pb_gm.GMSendMailReq()
    header = make_header(req.DESCRIPTOR.full_name)
    mail = req.mail_content
    mail.gm_uid = common.gid
    mail.addressee_type = mail_info.receive_type
    if mail_info.receive_type == 1:
        for item in mail_info.online_ids:
            mail.online_ids.append(item)
    elif mail_info.receive_type == 2:
        index = 0
        for item in mail_info.uids:
            mail.uids.append(item[0])
            mail.channels.append(item[1])
            index += 1
    mail.online_ids.append(mail_info.online_id)
    mail.sender = mail_info.sender.encode('utf-8')
    mail.title = mail_info.title.encode('utf-8')
    mail.content = mail_info.content.encode('utf-8')
    mail.valid_time = mail_info.valid_time
    mail.is_destroy = mail_info.is_destory
    mail.show_priority = (pb_gm.MailContent.Normal if mail_info.priority == 0
                          else pb_gm.MailContent.Top)
    mail.is_popping = mail_info.is_popping
    mail.delayed_time = mail_info.delayed_time
    for item in mail_info.attachments:
        attachment = mail.attachment_list.add()
        attachment.id = item[0]
        attachment.count = item[1]
    if len(mail.attachment_list) != 0:
        mail.mail_type = 1
    else:
        mail.mail_type = 0
    print(req)
    tcp_con.send(encode(header, req))


def unsend_mail():
    req = pb_gm.GMQueryUnsendMailReq()
    header = make_header(req.DESCRIPTOR.full_name)
    tcp_con.send(encode(header, req))


def del_unsend_mail(mail_id):
    req = pb_gm.GMDeleteUnsendMailReq()
    header = make_header(req.DESCRIPTOR.full_name)
    req.mail_ids.append(mail_id)
    tcp_con.send(encode(header, req))

