# !/usr/bin/python
# coding=utf-8

import csv


def ip_to_score(ip_address):
    score = 0
    for v in ip_address.split('.'):
        score = score * 256 + int(v, 10)
    return score


def import_ip_to_redis(filepath):
    with open(filepath, newline='', encoding='utf-8') as pcsv_file:
        csv_file = csv.DictReader(pcsv_file)
        for count, row in enumerate(csv_file):
            print(count, row)
            '''
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
            '''