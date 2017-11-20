# !/usr/bin/python
# coding=utf-8

import csv
import bisect


def ip_to_score(ip_address):
    score = 0
    for v in ip_address.split('.'):
        score = score * 256 + int(v, 10)
    return score


def import_ip_to_redis(filepath):
    with open(filepath, newline='', encoding='utf-8') as pcsv_file:
        csv_file = csv.DictReader(pcsv_file)
        for count, row in enumerate(csv_file):
            start_ip = row['geoname_id']
            if 'i' in start_ip.lower():
                continue
            if '.' in start_ip:
                start_ip = ip_to_score(start_ip)
            elif start_ip.isdigit():
                start_ip = int(start_ip, 10)
            else:
                continue
            city_id = row['country_name'] + '_' + str(count)
            print(start_ip, city_id)


# 自动补全
# 1.自动补全最近联系人(100人), 补全功能在python中实现, 适合少量数据类型
# * 最近联系人使用redis中列表保存 recent:user


def update_contact(conn, user, contacter):
    """
    更新最近联系人, lrem和ltrim时间复杂度都是o(n)
    """
    ac_list = 'recent:{}'.format(user)
    with conn.pipeline() as pipe:
        pipe.lrem(ac_list, contacter)
        pipe.lpush(ac_list, contacter)
        pipe.ltrim(ac_list, 0, 99)
        pipe.execute()


def remove_contact(conn, user, contacter):
    """
     删除最近联系人
    """
    conn.lrem('recent:{}'.format(user), contacter)


def autocomplete_contact(conn, user, prefix):
    candidates = conn.lrange('recent:{}'.format(user), 0, -1)
    matches = []
    for candidate in candidates:
        str_candidate = candidate.decode('utf-8')
        if str_candidate.lower().startswith(prefix):
            matches.append(str_candidate)
    return matches


# 2. 使用redis来实现自动补全(仅限字母), 自动补全列表使用redis中有序集合保存;
# 通过给定的前缀的最后一个字符, 可以得到前缀的前驱; 通过给前缀的末尾拼接上左花括号, 可以得到前缀的后继
valid_characters = '`abcdefghijklmnopqrstuvwsyz{'


def find_prefix_range(prefix):
    """
    根据输入前缀查询其前驱和后继
    """
    posn = bisect.bisect_left(valid_characters, prefix[-1:])
    suffix = valid_characters[posn or 1 - 1]
    return prefix[:-1] + suffix + '{', prefix + '{'

