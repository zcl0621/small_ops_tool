from __future__ import absolute_import

import jsonpath
from celery import shared_task

from public.file import logfile_to_name
from vpnstatus.models import VpnUser


@shared_task
def get_vpn_status():
    query_set = VpnUser.objects.all()
    online_list = logfile_to_name()
    for online_dict in online_list:
        if query_set.filter(username=online_dict['username']):
            vpn_user = query_set.get(username=online_dict['username'])
            if vpn_user.online:
                vpn_user.online_sum_time = vpn_user.online_sum_time + 60
            else:
                vpn_user.online = True
                vpn_user.save()
        else:
            VpnUser(username=online_dict['username'], cn_name=online_dict['cn_name'], online=True).save()
    for vpn_user in query_set.filter(online=True):
        if vpn_user.username in jsonpath.jsonpath(online_list, expr='$..username'):
            pass
        else:
            vpn_user.online = False
            vpn_user.save()
