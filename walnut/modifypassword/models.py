from django.db import models


# Create your models here.

class ModifyPassword(models.Model):
    username = models.CharField(max_length=20, null=False)
    cn_name = models.CharField(max_length=20, null=False)
    sms_code = models.CharField(max_length=20, null=False)
    updated = models.DateField(auto_now=True)

    class Meta:
        db_table = 'modify_password'
