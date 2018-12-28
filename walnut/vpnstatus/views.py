from rest_framework import viewsets

from vpnstatus.models import VpnUser
from vpnstatus.serializers import VpnUserSerializers


# Create your views here.
class VpnUserViewSet(viewsets.ModelViewSet):
    queryset = VpnUser.objects.all()
    serializer_class = VpnUserSerializers
