from rest_framework import serializers
from vpnstatus.models import VpnUser


class VpnUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = VpnUser
        fields = ('id', 'cn_name', 'username', 'online', 'online_sum_time')
        read_only_fields = ('id', 'username', 'cn_name', 'online', 'online_sum_time')
