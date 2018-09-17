#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#
from pdc.apps.utils.rpm import parse_nvr, parse_nvra

import django_filters
from django.db.models import Q
from django.core.exceptions import ValidationError

from pdc.apps.common.filters import value_is_not_empty, MultiValueFilter, CaseInsensitiveBooleanFilter, \
    MultiValueCaseInsensitiveFilter
from .models import Compose, OverrideRPM, ComposeTree, ComposeImage, VariantArch


class ComposeFilter(django_filters.FilterSet):
    release             = MultiValueCaseInsensitiveFilter(field_name='release__release_id')
    compose_id          = MultiValueCaseInsensitiveFilter(field_name='compose_id')
    compose_type        = MultiValueCaseInsensitiveFilter(field_name='compose_type__name')
    acceptance_testing  = MultiValueFilter(field_name='acceptance_testing__name')
    rpm_nvr             = django_filters.CharFilter(method="filter_nvr")
    rpm_nvra            = django_filters.CharFilter(method="filter_nvra")
    deleted             = CaseInsensitiveBooleanFilter()
    compose_date        = MultiValueFilter(field_name='compose_date')
    compose_respin      = MultiValueFilter(field_name='compose_respin')
    compose_label       = MultiValueFilter(field_name='compose_label')
    # TODO: return only latest compose

    @value_is_not_empty
    def filter_nvr(self, qs, name, value):
        try:
            nvr = parse_nvr(value)
        except ValueError:
            raise ValidationError("Invalid NVR: %s" % value)

        q = Q()
        q &= Q(variant__variantarch__composerpm__rpm__name=nvr["name"])
        q &= Q(variant__variantarch__composerpm__rpm__version=nvr["version"])
        q &= Q(variant__variantarch__composerpm__rpm__release=nvr["release"])
        return qs.filter(q).distinct()

    @value_is_not_empty
    def filter_nvra(self, qs, name, value):
        try:
            nvra = parse_nvra(value)
        except ValueError:
            raise ValidationError("Invalid NVRA: %s" % value)

        q = Q()
        q &= Q(variant__variantarch__composerpm__rpm__name=nvra["name"])
        q &= Q(variant__variantarch__composerpm__rpm__version=nvra["version"])
        q &= Q(variant__variantarch__composerpm__rpm__release=nvra["release"])
        q &= Q(variant__variantarch__composerpm__rpm__arch=nvra["arch"])
        return qs.filter(q).distinct()

    class Meta:
        model = Compose
        fields = ('deleted', 'compose_id', 'compose_date', 'compose_respin',
                  'compose_label', 'release', 'compose_type', 'acceptance_testing')


class OverrideRPMFilter(django_filters.FilterSet):
    release     = MultiValueCaseInsensitiveFilter(field_name='release__release_id')
    comment     = django_filters.CharFilter(lookup_expr='icontains')
    arch        = MultiValueFilter(field_name='arch')
    variant     = MultiValueFilter(field_name='variant')
    srpm_name   = MultiValueFilter(field_name='srpm_name')
    rpm_name    = MultiValueFilter(field_name='rpm_name')
    rpm_arch    = MultiValueFilter(field_name='rpm_arch')

    class Meta:
        model = OverrideRPM
        fields = ('release', 'variant', 'arch', 'srpm_name', 'rpm_name', 'rpm_arch', 'comment')


class ComposeTreeFilter(django_filters.FilterSet):
    compose         = MultiValueCaseInsensitiveFilter(field_name='compose__compose_id')
    variant         = MultiValueCaseInsensitiveFilter(field_name='variant__variant_uid')
    arch            = MultiValueCaseInsensitiveFilter(field_name='arch__name')
    location        = MultiValueCaseInsensitiveFilter(field_name='location__short')
    scheme          = MultiValueCaseInsensitiveFilter(field_name='scheme__name')

    class Meta:
        model = ComposeTree
        fields = ('compose', 'variant', 'arch', 'location', 'scheme')


class ComposeTreeRTTTestFilter(django_filters.FilterSet):
    compose         = MultiValueFilter(field_name='variant__compose__compose_id')
    variant         = MultiValueFilter(field_name='variant__variant_uid')
    arch            = MultiValueFilter(field_name='arch__name')
    test_result     = MultiValueFilter(field_name='rtt_testing_status__name')

    class Meta:
        model = VariantArch
        fields = ('compose', 'variant', 'arch', 'test_result')


class ComposeImageRTTTestFilter(django_filters.FilterSet):
    compose         = MultiValueFilter(field_name='variant_arch__variant__compose__compose_id')
    variant         = MultiValueFilter(field_name='variant_arch__variant__variant_uid')
    arch            = MultiValueFilter(field_name='variant_arch__arch__name')
    file_name       = MultiValueFilter(field_name='image__file_name')
    test_result     = MultiValueFilter(field_name='rtt_test_result__name')

    class Meta:
        model = ComposeImage
        fields = ('compose', 'variant', 'arch', 'file_name', 'test_result')
