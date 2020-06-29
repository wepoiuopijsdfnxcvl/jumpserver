# -*- coding: utf-8 -*-
#
from django.utils.translation import ugettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from .models import LoginPolicy


class LoginPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = LoginPolicy
        fields = ('', )