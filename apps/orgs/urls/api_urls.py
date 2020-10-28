# -*- coding: utf-8 -*-
#

from django.urls import re_path
from rest_framework.routers import DefaultRouter
from rest_framework_bulk.routes import BulkRouter

from common import api as capi
from .. import api


app_name = 'orgs'
router = DefaultRouter()
bulk_router = BulkRouter()

router.register(r'orgs', api.OrgViewSet, 'org')
bulk_router.register(r'org-memeber-relation', api.OrgMemberRelationBulkViewSet, 'org-memeber-relation')

# 将会删除
router.register(r'orgs/(?P<org_id>[0-9a-zA-Z\-]{36})/membership/admins',
                api.OrgMembershipAdminsViewSet, 'membership-admins')
router.register(r'orgs/(?P<org_id>[0-9a-zA-Z\-]{36})/membership/users',
                api.OrgMembershipUsersViewSet, 'membership-users'),

old_version_urlpatterns = [
    re_path('(?P<resource>org)/.*', capi.redirect_plural_name_api)
]

urlpatterns = router.urls + bulk_router.urls + old_version_urlpatterns
