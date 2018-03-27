#
# Copyright (c) 2018 Red Hat
# Licensed under The MIT License (MIT)
# https://opensource.org/licenses/MIT
#
from contrib import drf_introspection

from django_filters import NumberFilter
from rest_framework.utils import formatting

LOOKUP_TYPES = {
    'icontains': 'case insensitive, substring match',
    'contains': 'substring match',
    'iexact': 'case insensitive',
}


def get_filters(view):
    """
    For a given view set returns which query filters are available for it a
    Markdown formatted list. The list does not include query filters specified
    on serializer or query arguments used for paging.
    """
    allowed_keys = drf_introspection.get_allowed_query_params(view)
    serializer_class = getattr(view, 'serializer_class', None)
    filter_class = getattr(view, 'filter_class', None)
    filterset = filter_class() if filter_class is not None else None
    filterset_fields = filterset.filters if filterset is not None else []

    filters = []
    for key in sorted(allowed_keys):
        if key in filterset_fields:
            # filter defined in FilterSet
            filter_ = filterset_fields.get(key)
            doc = _get_filter(key, filter_)
            filters.append(doc)
        else:
            doc = ' * `%s`' % key
            doc_attribute_name = 'doc_query_param_' + key
            description = getattr(view, doc_attribute_name, '')
            if not description and serializer_class:
                description = getattr(serializer_class, doc_attribute_name, '')
            if description:
                doc += ' ' + formatting.dedent(description)
            filters.append(doc)

    return '\n'.join(filters)


def _get_filter_option(filter, option_name):
    value = getattr(filter, option_name, '') or filter.extra.get(option_name, '')
    return value.rstrip()


def _get_filter(filter_name, filter):
    filter_type = _get_filter_option(filter, 'doc_format')
    if not filter_type:
        if isinstance(filter, NumberFilter):
            filter_type = 'int'
        else:
            filter_type = 'string'

    lookup_type = LOOKUP_TYPES.get(filter.lookup_expr)
    if lookup_type:
        lookup_type = ', %s' % lookup_type

    result = ' * `%s` (%s%s)' % (filter_name, filter_type, lookup_type or '')
    help_text = _get_filter_option(filter, 'help_text')
    if help_text:
        result += ' ' + help_text

    return result
