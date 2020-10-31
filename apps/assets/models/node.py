# -*- coding: utf-8 -*-
#
import uuid

from django.db import models, transaction
from django.db.models import Q, F, Case, When
from django.db.utils import IntegrityError
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ugettext
from django.db.transaction import atomic

from common.struct import Stack
from common.utils import get_logger
from common.utils.common import lazyproperty
from orgs.mixins.models import OrgModelMixin, OrgManager
from orgs.utils import get_current_org, tmp_to_org
from orgs.models import Organization


__all__ = ['Node', 'FamilyMixin']
logger = get_logger(__name__)


class NodeQuerySet(models.QuerySet):
    def delete(self):
        raise NotImplementedError


class FamilyMixin:
    __parents = None
    __children = None
    __all_children = None
    is_node = True

    def get_next_child_preset_name(self):
        name = ugettext("New node")
        values = [
            child.value[child.value.rfind(' '):]
            for child in self.get_children()
            if child.value.startswith(name)
        ]
        values = [int(value) for value in values if value.strip().isdigit()]
        count = max(values) + 1 if values else 1
        return '{} {}'.format(name, count)

    def get_siblings(self, with_self=False):
        key = ':'.join(self.key.split(':')[:-1])
        pattern = r'^{}:[0-9]+$'.format(key)
        sibling = Node.objects.filter(
            key__regex=pattern.format(self.key)
        )
        if not with_self:
            sibling = sibling.exclude(key=self.key)
        return sibling

    def get_family(self):
        ancestors = self.get_ancestors()
        children = self.get_all_children()
        return [*tuple(ancestors), self, *tuple(children)]


class NodeAssetsMixin:
    key = ''
    id = None

    def get_all_assets(self):
        from .asset import Asset
        q = Q(nodes__key__startswith=f'{self.key}:') | Q(nodes__key=self.key)
        return Asset.objects.filter(q).distinct()

    @classmethod
    def get_node_all_assets_by_key_v2(cls, key):
        # 最初的写法是：
        #   Asset.objects.filter(Q(nodes__key__startswith=f'{node.key}:') | Q(nodes__id=node.id))
        #   可是 startswith 会导致表关联时 Asset 索引失效
        from .asset import Asset
        node_ids = cls.objects.filter(
            Q(key__startswith=f'{key}:') |
            Q(key=key)
        ).values_list('id', flat=True).distinct()
        assets = Asset.objects.filter(
            nodes__id__in=list(node_ids)
        ).distinct()
        return assets

    def get_assets(self):
        from .asset import Asset
        assets = Asset.objects.filter(nodes=self)
        return assets.distinct()

    def get_valid_assets(self):
        return self.get_assets().valid()

    def get_all_valid_assets(self):
        return self.get_all_assets().valid()

    @classmethod
    def get_nodes_all_assets_ids(cls, nodes_keys):
        assets_ids = cls.get_nodes_all_assets(nodes_keys).values_list('id', flat=True)
        return assets_ids

    @classmethod
    def get_nodes_all_assets(cls, nodes_keys, extra_assets_ids=None):
        from .asset import Asset
        nodes_keys = cls.clean_children_keys(nodes_keys)
        q = Q()
        node_ids = ()
        for key in nodes_keys:
            q |= Q(key__startswith=f'{key}:')
            q |= Q(key=key)
        if q:
            node_ids = Node.objects.filter(q).distinct().values_list('id', flat=True)

        q = Q(nodes__id__in=list(node_ids))
        if extra_assets_ids:
            q |= Q(id__in=extra_assets_ids)
        if q:
            return Asset.org_objects.filter(q).distinct()
        else:
            return Asset.objects.none()


class SomeNodesMixin:
    key = ''
    default_key = '1'
    default_value = 'Default'
    empty_key = '-11'
    empty_value = _("empty")

    @classmethod
    def default_node(cls):
        with tmp_to_org(Organization.default()):
            defaults = {'value': cls.default_value}
            try:
                obj, created = cls.objects.get_or_create(
                    defaults=defaults, key=cls.default_key,
                )
            except IntegrityError as e:
                logger.error("Create default node failed: {}".format(e))
                cls.modify_other_org_root_node_key()
                obj, created = cls.objects.get_or_create(
                    defaults=defaults, key=cls.default_key,
                )
            return obj

    def is_default_node(self):
        return self.key == self.default_key

    def is_org_root(self):
        if self.key.isdigit():
            return True
        else:
            return False

    @classmethod
    def get_next_org_root_node_key(cls):
        with tmp_to_org(Organization.root()):
            org_nodes_roots = cls.objects.filter(key__regex=r'^[0-9]+$')
            org_nodes_roots_keys = org_nodes_roots.values_list('key', flat=True)
            if not org_nodes_roots_keys:
                org_nodes_roots_keys = ['1']
            max_key = max([int(k) for k in org_nodes_roots_keys])
            key = str(max_key + 1) if max_key != 0 else '2'
            return key

    @classmethod
    def create_org_root_node(cls):
        # 如果使用current_org 在set_current_org时会死循环
        ori_org = get_current_org()
        with transaction.atomic():
            if not ori_org.is_real():
                return cls.default_node()
            key = cls.get_next_org_root_node_key()
            root = cls.objects.create(key=key, value=ori_org.name)
            return root

    @classmethod
    def org_root(cls):
        root = cls.objects.filter(parent_key='').exclude(key__startswith='-')
        if root:
            return root[0]
        else:
            return cls.create_org_root_node()

    @classmethod
    def initial_some_nodes(cls):
        cls.default_node()

    @classmethod
    def modify_other_org_root_node_key(cls):
        """
        解决创建 default 节点失败的问题，
        因为在其他组织下存在 default 节点，故在 DEFAULT 组织下 get 不到 create 失败
        """
        logger.info("Modify other org root node key")

        with tmp_to_org(Organization.root()):
            node_key1 = cls.objects.filter(key='1').first()
            if not node_key1:
                logger.info("Not found node that `key` = 1")
                return
            if not node_key1.org.is_real():
                logger.info("Org is not real for node that `key` = 1")
                return

        with transaction.atomic():
            with tmp_to_org(node_key1.org):
                org_root_node_new_key = cls.get_next_org_root_node_key()
                for n in cls.objects.all():
                    old_key = n.key
                    key_list = n.key.split(':')
                    key_list[0] = org_root_node_new_key
                    new_key = ':'.join(key_list)
                    n.key = new_key
                    n.save()
                    logger.info('Modify key ( {} > {} )'.format(old_key, new_key))


class Node(OrgModelMixin, SomeNodesMixin, FamilyMixin, NodeAssetsMixin):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True)
    key = models.CharField(unique=True, max_length=64, verbose_name=_("Key"))  # '1:1:1:1'
    value = models.CharField(max_length=128, verbose_name=_("Value"))
    child_mark = models.IntegerField(default=0)
    date_create = models.DateTimeField(auto_now_add=True)
    parent_key = models.CharField(max_length=64, verbose_name=_("Parent key"),
                                  db_index=True, default='')
    assets_amount = models.IntegerField(default=0)
    left = models.IntegerField(default=0, null=False, db_index=True)
    right = models.IntegerField(default=0, null=False, db_index=True)
    level = models.IntegerField(default=0, null=False, db_index=True)
    parent = models.ForeignKey('self', db_constraint=False, on_delete=models.PROTECT,
                               default=None, null=True, related_name='children')

    objects = OrgManager.from_queryset(NodeQuerySet)()
    is_node = True
    _parents = None

    class Meta:
        verbose_name = _("Node")
        ordering = ['key']

    def __str__(self):
        return self.value

    def __gt__(self, other):
        self_key = [int(k) for k in self.key.split(':')]
        other_key = [int(k) for k in other.key.split(':')]
        self_parent_key = self_key[:-1]
        other_parent_key = other_key[:-1]

        if self_parent_key and self_parent_key == other_parent_key:
            return self.value > other.value
        return self_key > other_key

    def __lt__(self, other):
        return not self.__gt__(other)

    @property
    def name(self):
        return self.value

    @lazyproperty
    def full_value(self):
        # 不要在列表中调用该属性
        values = self.get_ancestors().values_list('value')
        return ' / '.join(values)

    def as_tree_node(self):
        from common.tree import TreeNode
        name = '{} ({})'.format(self.value, self.assets_amount)
        data = {
            'id': self.key,
            'name': name,
            'title': name,
            'pId': self.parent_key,
            'isParent': True,
            'open': self.is_org_root(),
            'meta': {
                'node': {
                    "id": self.id,
                    "name": self.name,
                    "value": self.value,
                    "key": self.key,
                    "assets_amount": self.assets_amount,
                },
                'type': 'node'
            }
        }
        tree_node = TreeNode(**data)
        return tree_node

    def has_children_or_has_assets(self):
        if self.children or self.get_assets().exists():
            return True
        return False

    def delete(self, using=None, keep_parents=False):
        if self.has_children_or_has_assets():
            return
        return super().delete(using=using, keep_parents=keep_parents)

    @property
    def ancestors(self):
        return self.get_ancestors(with_self=False)

    def get_ancestors(self, with_self=False):
        if with_self:
            q = Q(left__lte=self.left, right__gte=self.right)
        else:
            q = Q(left__lt=self.left, right__gt=self.right)

        org = get_current_org()
        if not org or org.is_root():
            q &= Q(org_id=self.org_id)

        return self.__class__.objects.filter(q).order_by('left')

    def get_descendant(self, with_self=False):
        if with_self:
            q = Q(left__gte=self.left, right__lte=self.right)
        else:
            q = Q(left__gt=self.left, right__lt=self.right)

        org = get_current_org()
        if not org or org.is_root():
            q &= Q(org_id=self.org_id)

        return self.__class__.objects.filter(q)

    @property
    def descendant(self):
        return self.get_descendant(with_self=False)

    def create_child(self, value=None, _id=None):
        with atomic(savepoint=False):
            index = self.right
            self._update_mptt_serial(index)
            child = self.__class__.objects.create(
                id=_id, value=value, parent=self,
                left=index, right=index + 1, level=self.level+1
            )
            return child

    def get_or_create_child(self, value, _id=None):
        """
        :return: Node, bool (created)
        """
        children = self.children
        exist = children.filter(value=value).exists()
        if exist:
            child = children.filter(value=value).first()
            created = False
        else:
            child = self.create_child(value, _id)
            created = True
        return child, created

    @property
    def parent(self):
        if self.is_org_root():
            return self
        return self.parent

    def _update_mptt_serial(self, index, offset=2):
        to_update_nodes = Node.objects.filter(
            right__gte=index
        )
        to_update_nodes.update(
            right=F('right') + offset,
            left=Case(
                When(left__gt=index, then=F('left') + index),
                default=F('left'),
                output_field=models.IntegerField()
            )
        )

    def init_mptt_tree(self, node, index=1):
        pass

    @parent.setter
    def parent(self, parent):
        with transaction.atomic(savepoint=False):
            parent: Node
            self: Node

            offset = self.right - self.left + 1
            self._update_mptt_serial(parent.right, offset)
