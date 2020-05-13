
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from users.models import User, UserGroup
from assets.models import Asset, Domain, AdminUser, SystemUser, Label
from perms.models import AssetPermission
from common.serializers import AdaptedBulkListSerializer
from .utils import tmp_to_org
from .models import Organization
from .mixins.serializers import OrgMembershipSerializerMixin


class OrgSerializer(ModelSerializer):
    class Meta:
        model = Organization
        list_serializer_class = AdaptedBulkListSerializer
        fields_mini = ['id', 'name']
        fields_small = fields_mini + ['comment', 'created_by', 'date_created']
        fields = fields_small
        read_only_fields = ['created_by', 'date_created']


class OrgReadSerializer(ModelSerializer):
    admins_amount = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    auditors_amount = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    users_amount = serializers.SlugRelatedField(slug_field='name', many=True, read_only=True)
    user_groups_amount = serializers.SerializerMethodField()
    assets_amount = serializers.SerializerMethodField()
    domains_amount = serializers.SerializerMethodField()
    admin_users_amount = serializers.SerializerMethodField()
    system_users_amount = serializers.SerializerMethodField()
    labels_amount = serializers.SerializerMethodField()
    perms_amount = serializers.SerializerMethodField()

    class Meta:
        model = Organization
        fields = '__all__'

    @staticmethod
    def get_org_resource_amount(obj, model):
        with tmp_to_org(obj):
            return model.objects.all().count()

    def get_user_groups_amount(self, obj):
        return self.get_org_resource_amount(obj, UserGroup)

    def get_assets(self, obj):
        return self.get_org_resource_amount(obj, Asset)

    def get_domains(self, obj):
        return self.get_org_resource_amount(obj, Domain)

    def get_admin_users(self, obj):
        return self.get_org_resource_amount(obj, AdminUser)

    def get_system_users(self, obj):
        return self.get_org_resource_amount(obj, SystemUser)

    def get_labels(self, obj):
        return self.get_org_resource_amount(obj, Label)

    def get_perms(self, obj):
        return self.get_org_resource_amount(obj, AssetPermission)


class OrgMembershipAdminSerializer(OrgMembershipSerializerMixin, ModelSerializer):
    class Meta:
        # model = Organization.admins.through
        list_serializer_class = AdaptedBulkListSerializer
        fields = '__all__'


class OrgMembershipUserSerializer(OrgMembershipSerializerMixin, ModelSerializer):
    class Meta:
        # model = Organization.users.through
        list_serializer_class = AdaptedBulkListSerializer
        fields = '__all__'


class OrgAllUserSerializer(serializers.Serializer):
    user = serializers.UUIDField(read_only=True, source='id')
    user_display = serializers.SerializerMethodField()

    class Meta:
        only_fields = ['id', 'username', 'name']

    @staticmethod
    def get_user_display(obj):
        return str(obj)
