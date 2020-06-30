from orgs.mixins.api import OrgBulkModelViewSet

from .models import AccessControl
from .serializers import LoginPolicySerializer


class LoginPolicyViewSet(OrgBulkModelViewSet):
    model = AccessControl
    serializer_class = LoginPolicySerializer
