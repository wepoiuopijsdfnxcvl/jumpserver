from django.db import models
from django.urls import reverse

from orgs.mixins.models import OrgModelMixin


class AccessControl(OrgModelMixin):
    name = models.CharField(max_length=512)
    ips = models.CharField(max_length=512)
    date_from = models.DateTimeField()
    date_to = models.DateTimeField()
    users = models.ManyToManyField('users.User', related_name='login_policies')

    def get_absolute_url(self):
        return reverse('api-access-control:access-control-detail', args=(self.id,))
