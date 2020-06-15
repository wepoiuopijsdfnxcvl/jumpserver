import uuid

from django.db import models
from django.utils.translation import ugettext_lazy as _

from common.utils import is_uuid


class Organization(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=128, unique=True, verbose_name=_("Name"))
    created_by = models.CharField(max_length=32, null=True, blank=True, verbose_name=_('Created by'))
    date_created = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name=_('Date created'))
    comment = models.TextField(max_length=128, default='', blank=True, verbose_name=_('Comment'))
    members = models.ManyToManyField('users.User', related_name='orgs', through='orgs.OrganizationMembers', through_fields=('org', 'user'))

    orgs = None
    CACHE_PREFIX = 'JMS_ORG_{}'
    ROOT_ID = '00000000-0000-0000-0000-000000000000'
    ROOT_NAME = 'ROOT'
    DEFAULT_ID = 'DEFAULT'
    DEFAULT_NAME = 'DEFAULT'
    SYSTEM_ID = '00000000-0000-0000-0000-000000000002'
    SYSTEM_NAME = 'SYSTEM'
    _user_admin_orgs = None

    class Meta:
        verbose_name = _("Organization")

    def __str__(self):
        return self.name

    def get_resource_amount(self, resource_model):
        from .utils import tmp_to_org
        from .mixins.models import OrgModelMixin

        if not issubclass(resource_model, OrgModelMixin):
            return 0
        with tmp_to_org(self):
            return resource_model.objects.all().count()

    def get_total_resources_amount(self):
        from django.apps import apps
        from .mixins.models import OrgModelMixin
        summary = {'users.Members': self.members.all().count()}
        for app_name, app_config in apps.app_configs.items():
            models_cls = app_config.get_models()
            for model in models_cls:
                if not issubclass(model, OrgModelMixin):
                    continue
                key = '{}.{}'.format(app_name, model.__name__)
                summary[key] = self.get_resource_amount(model)
        return summary

    def has_resource(self):
        summary = self.get_total_resources_amount()
        for tp, amount in summary.items():
            if amount != 0:
                return True
        return False

    def set_to_cache(self):
        if self.__class__.orgs is None:
            self.__class__.orgs = {}
        self.__class__.orgs[str(self.id)] = self

    def expire_cache(self):
        self.__class__.orgs.pop(str(self.id), None)

    @classmethod
    def get_instance_from_cache(cls, oid):
        if not cls.orgs or not isinstance(cls.orgs, dict):
            return None
        return cls.orgs.get(str(oid))

    @classmethod
    def get_instance(cls, id_or_name, default=False):
        cached = cls.get_instance_from_cache(id_or_name)
        if cached:
            return cached

        if id_or_name is None:
            return cls.default() if default else None
        elif id_or_name in [cls.DEFAULT_ID, cls.DEFAULT_NAME, '']:
            return cls.default()
        elif id_or_name in [cls.ROOT_ID, cls.ROOT_NAME]:
            return cls.root()
        elif id_or_name in [cls.SYSTEM_ID, cls.SYSTEM_NAME]:
            return cls.system()

        try:
            if is_uuid(id_or_name):
                org = cls.objects.get(id=id_or_name)
            else:
                org = cls.objects.get(name=id_or_name)
            org.set_to_cache()
        except cls.DoesNotExist:
            org = cls.default() if default else None
        return org

    def org_id(self):
        if self.is_real():
            return self.id
        elif self.is_root():
            return self.ROOT_ID
        else:
            return ''

    def get_org_auditors(self):
        return self.members.filter(role=OrganizationMembers.ROLE_AUDITOR)

    def get_org_members(self, role=None):
        from users.models import User
        kwargs = {'org': self}
        if role:
            kwargs['role'] = role
        users_id = OrganizationMembers.objects.filter(**kwargs).values_list('user')
        return User.objects.filter(id__in=users_id)

    def can_admin_by(self, user):
        if user.is_superuser:
            return True
        if self.get_org_members(role=OrganizationMembers.ROLE_ADMIN).filter(id=user.id):
            return True
        return False

    def can_audit_by(self, user):
        if user.is_super_auditor:
            return True
        if self.get_org_auditors().filter(id=user.id):
            return True
        return False

    def is_real(self):
        return self.id not in (self.DEFAULT_NAME, self.ROOT_ID, self.SYSTEM_ID)

    @classmethod
    def get_user_joined_orgs(cls, user, roles=None):
        if user.is_anonymous:
            return cls.objects.none()
        kwargs = {'user': user}
        if roles:
            kwargs['role__in'] = roles
        orgs_id = OrganizationMembers.objects.filter(**kwargs).values_list('org', flat=True)
        return cls.objects.filter(id__in=orgs_id)

    @classmethod
    def get_user_admin_or_audit_orgs(cls, user):
        roles = [OrganizationMembers.ROLE_ADMIN, OrganizationMembers.ROLE_AUDITOR]
        return cls.get_user_joined_orgs(user, roles=roles)

    @classmethod
    def default(cls):
        return cls(id=cls.DEFAULT_ID, name=cls.DEFAULT_NAME)

    @classmethod
    def root(cls):
        return cls(id=cls.ROOT_ID, name=cls.ROOT_NAME)

    @classmethod
    def system(cls):
        return cls(id=cls.SYSTEM_ID, name=cls.SYSTEM_NAME)

    def is_root(self):
        return self.id is self.ROOT_ID

    def is_default(self):
        return self.id is self.DEFAULT_ID

    def is_system(self):
        return self.id is self.SYSTEM_ID

    def change_to(self):
        from .utils import set_current_org
        set_current_org(self)

    @classmethod
    def all_orgs(cls):
        orgs = list(cls.objects.all())
        orgs.append(cls.default())
        return orgs


class OrganizationMembers(models.Model):
    ROLE_ADMIN = 'Admin'
    ROLE_USER = 'User'
    ROLE_AUDITOR = 'Auditor'

    ROLE_CHOICES = (
        (ROLE_ADMIN, _('Administrator')),
        (ROLE_USER, _('User')),
        (ROLE_AUDITOR, _("Auditor"))
    )
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    org = models.ForeignKey(Organization, on_delete=models.CASCADE, verbose_name=_('Organization'))
    user = models.ForeignKey('users.User', on_delete=models.CASCADE, verbose_name=_('User'))
    role = models.CharField(max_length=16, choices=ROLE_CHOICES, default=ROLE_USER, verbose_name=_("Role"))
    date_created = models.DateTimeField(auto_now_add=True, verbose_name=_("Date created"))
    date_updated = models.DateTimeField(auto_now=True, verbose_name=_("Date updated"))
    created_by = models.CharField(max_length=128, null=True, verbose_name=_('Created by'))

    class Meta:
        unique_together = [('org', 'user', 'role')]
        db_table = 'orgs_organization_members'

    def __str__(self):
        return '{} is {}: {}'.format(self.user.name, self.org.name, self.role)
