from orgs.mixins.api import OrgBulkModelViewSet

from .models import LoginPolicy
from .serializers import LoginPolicySerializer


class LoginPolicyViewSet(OrgBulkModelViewSet):
    model = LoginPolicy
    serializer_class = LoginPolicySerializer
