from django.db import models


class LoginPolicy(models.Model):
    name = models.CharField(max_length=512)
    ips = models.CharField(max_length=512)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    users = models.ManyToManyField('users.User', related_name='login_policies')

