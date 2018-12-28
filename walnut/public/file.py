# -*- coding=utf-8 -*-
import re

from public.ldap import PublicLdap
from walnut.settings import vpn_status_log


def logfile_to_name():
    file = open(vpn_status_log)
    file_online_list = []
    for line in file:
        if logfile_to_dict(line):
            file_online_list.append(logfile_to_dict(line))
    file.close()
    return file_online_list


def logfile_to_dict(line):
    try:
        line_list = line.split(",")
        matchObj = re.match(
            '(?<![0-9])(?:(?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})[.](?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})[.](?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2})[.](?:25[0-5]|2[0-4][0-9]|[0-1]?[0-9]{1,2}))(?![0-9])',
            line_list[0], re.M | re.I)
        # 判断是否为ip开头
        if matchObj:
            username = line_list[1]
            cn_name = PublicLdap(find_username=username).cn
            if username and cn_name:
                return {"username": username, "cn_name": cn_name}
    except Exception as e:
        print(e)
        pass
