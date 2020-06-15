
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from common.serializers import AdaptedBulkListSerializer
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
        extra_kwargs = {
            'admins': {'write_only': True},
            'users': {'write_only': True},
            'auditors': {'write_only': True},
        }

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


class OrgRetrieveSerializer(OrgReadSerializer):
    admins = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    auditors = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    users = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta(OrgReadSerializer.Meta):
        pass
