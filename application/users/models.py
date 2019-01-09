from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    name = models.CharField(blank=True, max_length=255)
    mobile = models.CharField(blank=True, max_length=15)
    otp = models.CharField(blank=True, max_length=4)

    def __str__(self):
        return str(self.mobile)


class AuthUserLog(models.Model):
    ip_address = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'auth_user_log'

    def __str__(self):
        return self.ip_address