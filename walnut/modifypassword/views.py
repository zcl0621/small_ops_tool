from rest_framework import viewsets, status
from rest_framework.response import Response

from modifypassword.models import ModifyPassword
from modifypassword.serializers import ModifyPasswordSerializers
from public.ldap import PublicLdap
from public.sms import AliSMS, sms_code


# Create your views here.
class ModifyPasswordViewSet(viewsets.ModelViewSet):
    queryset = ModifyPassword.objects.all()
    serializer_class = ModifyPasswordSerializers

    def list(self, request, *args, **kwargs):
        find_username = request.query_params.get('username', None)
        if find_username:
            ldap = PublicLdap(find_username=find_username)
            if type(ldap.telephoneNumber) is not dict and type(ldap.cn) is not dict:
                code = sms_code()
                if code:
                    sms = AliSMS(code=code, phone=ldap.telephoneNumber)
                    resp = sms.send()
                    if resp.status_code == 200:
                        query_set = ModifyPassword.objects.all()
                        if query_set.filter(username=find_username):
                            user = query_set.get(username=find_username)
                            user.sms_code = code
                            user.save()
                        else:
                            ModifyPassword(username=find_username, cn_name=ldap.cn, sms_code=code).save()
                    return Response(data={'code': code, 'cn_name': ldap.cn}, status=status.HTTP_200_OK)
                else:
                    return Response(data={'data': '短信发送失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data=ldap.telephoneNumber, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        username = self.request.data.get('username', None)
        cn_name = self.request.data.get('cn_name', None)
        sms_code = self.request.data.get('sms_code', None)
        password = self.request.data.get('password', None)
        if username and cn_name and sms_code and password:
            query = ModifyPassword.objects.get(username=username)
            if query.sms_code == sms_code:
                ldap = PublicLdap(find_username=username, new_password=password)
                modify_res = ldap.modify_password()
                if modify_res['status']:
                    return Response(data=modify_res, status=status.HTTP_200_OK)
                else:
                    return Response(data=modify_res, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data={'data': '短信验证码错误'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'data': '参数不全'}, status=status.HTTP_400_BAD_REQUEST)
