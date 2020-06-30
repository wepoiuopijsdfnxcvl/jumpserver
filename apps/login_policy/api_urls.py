from rest_framework_bulk.routes import BulkRouter

from .api import LoginPolicyViewSet

app_name = 'login-policy'

router = BulkRouter()
router.register('login-policies', LoginPolicyViewSet, 'login-policy')

urlpatterns = router.urls
