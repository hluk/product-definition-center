#
# Copyright (c) 2015 Red Hat
# Licensed under The MIT License (MIT)
# http://opensource.org/licenses/MIT
#

from inspect import getmro


def _get_fields(class_, attribute_name):
    all_keys = set()
    fields = []
    for base_class in reversed(getmro(class_)):
        keys = set(getattr(base_class, attribute_name, set())) - all_keys
        all_keys.update(keys)
        fields += keys
    return reversed(fields)


def get_allowed_query_params(view):
    """
    The list of allowed parameters is obtained from multiple sources:

      * filter set class
      * extra_query_params attribute (which should be a list/tuple of strings)
      * paginate_by_param attribute

    The serializer can define what query parameters it uses by defining a
    `query_params` class attribute on the serializer. Note that this should
    only include the parameters that are passed via URL query string, not
    request body fields.
    """

    allowed_keys = []

    # Take all filters from filter set.
    filter_class = getattr(view, 'filter_class', None)
    if filter_class:
        filter_set = filter_class()
        allowed_keys += sorted(filter_set.filters.keys())
    # Take extra params specified on viewset.
    allowed_keys += _get_fields(view.__class__, 'extra_query_params')
    # Add pagination param.
    if hasattr(view, 'paginator'):
        page = getattr(view.paginator, 'page_query_param', None)
        if page:
            allowed_keys.append(page)
        page_size = getattr(view.paginator, 'page_size_query_param', None)
        if page_size:
            allowed_keys.append(page_size)

    # Add fields from serializer if specified.
    serializer_class = getattr(view, 'serializer_class', None)
    if serializer_class:
        allowed_keys += _get_fields(serializer_class, 'query_params')

    return allowed_keys
