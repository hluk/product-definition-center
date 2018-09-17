#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
import re

from django.contrib.auth import models

import django_filters

from pdc.apps.common.filters import MultiValueFilter
from .models import GroupResourcePermission, ResourcePermission, ResourceApiUrl


class PermissionFilter(django_filters.FilterSet):
    codename        = MultiValueFilter()
    app_label       = MultiValueFilter(field_name='content_type__app_label',
                                       distinct=True)
    model           = MultiValueFilter(field_name='content_type__model',
                                       distinct=True)

    class Meta:
        model = models.Permission
        fields = ('codename', 'app_label', 'model')


class GroupFilter(django_filters.FilterSet):
    name                  = MultiValueFilter()
    permission_codename   = MultiValueFilter(field_name='permissions__codename',
                                             distinct=True)
    permission_app_label  = MultiValueFilter(field_name='permissions__content_type__app_label',
                                             distinct=True)
    permission_model      = MultiValueFilter(field_name='permissions__content_type__model',
                                             distinct=True)

    class Meta:
        model = models.Group
        fields = ('name', 'permission_codename',
                  'permission_app_label', 'permission_model')


class GroupResourcePermissionFilter(django_filters.FilterSet):
    group = MultiValueFilter(field_name='group__name')
    permission = MultiValueFilter(field_name='resource_permission__permission__name')
    resource = MultiValueFilter(field_name='resource_permission__resource__name')

    class Meta:
        model = GroupResourcePermission
        fields = ('group', 'resource', 'permission')


class ResourcePermissionFilter(django_filters.FilterSet):
    permission = MultiValueFilter(field_name='permission__name')
    resource = MultiValueFilter(field_name='resource__name')

    class Meta:
        model = ResourcePermission
        fields = ('resource', 'permission')


class ResourceFilter(MultiValueFilter):
    def _filter(self, qs, name, value):
        for resource_name in value:
            regex = re.sub(r'{.*?}', r'(.*?)', resource_name)
            if regex != resource_name:
                qs = qs.filter(**{self.field_name + '__regex': regex})
            else:
                qs = super(ResourceFilter, self)._filter(qs, name, value)
        return qs


class ResourceApiUrlFilter(django_filters.FilterSet):
    resource = ResourceFilter(field_name='resource__name')
    url = MultiValueFilter()

    class Meta:
        model = ResourceApiUrl
        fields = ('resource', 'url')
