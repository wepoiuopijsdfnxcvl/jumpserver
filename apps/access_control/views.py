from django.shortcuts import render

# Create your views here.
# coding: utf-8
#

from django.http import Http404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView
from django.utils.translation import ugettext_lazy as _
from django.views.generic.detail import DetailView

from common.permissions import PermissionsMixin, IsOrgAdmin, IsValidUser
from .models import AccessControl
from .forms import AccessControlForm


class AccessControlListView(PermissionsMixin, TemplateView):
    template_name = 'access_control/access_control_list.html'
    permission_classes = [IsOrgAdmin]


class AccessControlCreateView(CreateView):
    template_name = 'access_control/access_control_create_update.html'
    form_class = AccessControlForm

#
# class DatabaseAppUpdateView(BaseDatabaseAppCreateUpdateView, UpdateView):
#
#     def get_type(self):
#         return self.object.type
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'app': _('Applications'),
#             'action': _('Create DatabaseApp'),
#             'api_action': 'update'
#         }
#         kwargs.update(context)
#         return super().get_context_data(**kwargs)
#
#
# class DatabaseAppDetailView(PermissionsMixin, DetailView):
#     template_name = 'applications/database_app_detail.html'
#     model = models.DatabaseApp
#     context_object_name = 'database_app'
#     permission_classes = [IsOrgAdmin]
#
#     def get_context_data(self, **kwargs):
#         context = {
#             'app': _('Applications'),
#             'action': _('DatabaseApp detail'),
#         }
#         kwargs.update(context)
#         return super().get_context_data(**kwargs)
