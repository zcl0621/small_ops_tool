from django.db import models


# Create your models here.
class VpnUser(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=256, null=False)
    cn_name = models.CharField(max_length=256, null=False)
    online = models.BooleanField(default=False)
    online_sum_time = models.IntegerField(null=False, default=0)

    class Meta:
        db_table = 'vpnuser'
