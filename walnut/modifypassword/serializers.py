from rest_framework import serializers
from modifypassword.models import ModifyPassword


class ModifyPasswordSerializers(serializers.ModelSerializer):
    class Meta:
        model = ModifyPassword
        fields = ('id', 'username', 'cn_name', 'sms_code', 'updated')
        read_only_fields = ('id', 'updated')
