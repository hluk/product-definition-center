import re
from restfw_composed_permissions.base import BasePermissionComponent, BaseComposedPermision
from restfw_composed_permissions.generic.components import AllowAll
from django.conf import settings

from pdc.apps.auth.models import Resource, GroupResourcePermission
from pdc.apps.utils.utils import read_permission_for_all


class APIPermissionComponent(BasePermissionComponent):
    """
    Allow only anonymous requests.
    """

    def has_permission(self, permission, request, view):
        if request.user.is_superuser or (hasattr(settings, 'DISABLE_RESOURCE_PERMISSION_CHECK') and
                                         settings.DISABLE_RESOURCE_PERMISSION_CHECK):
            return True
        api_name = request.path.replace("%s%s/" % (settings.REST_API_URL, settings.REST_API_VERSION), '').strip('/')
        internal_permission = self._convert_permission(request.method)
        if not internal_permission or (read_permission_for_all() and internal_permission == 'read'):
            return True
        return self._has_permission(internal_permission, request.user, str(view.__class__), api_name)

    def _has_permission(self, internal_permission, user, view, api_name):
        resource = self._find_resource(view, api_name)

        if resource is None:
            # Do not restrict access to resource that is not in permission control.
            return True

        group_id_list = [group.id for group in user.groups.all()]
        result = GroupResourcePermission.objects.filter(
            group__id__in=group_id_list, resource_permission__resource=resource,
            resource_permission__permission__name=internal_permission).exists()
        return result

    @staticmethod
    def _find_resource(view, api_name):
        resources = Resource.objects.filter(view=view)

        if len(resources) == 1:
            return resources[0]

        if len(resources) > 1:
            # Multiple APIs map to single view.
            resources2 = resources.filter(name=api_name)
            if len(resources2) == 1:
                return resources2[0]

            # Try fuzzy match resource name (i.e. resource prefix is regex).
            return APIPermissionComponent._try_regexp_resource_match(api_name, resources)

        return None

    @staticmethod
    def _try_regexp_resource_match(api_name, resources):
        for resource_obj in resources:
            pattern = re.sub(r'{.*?}', r'(.*?)', resource_obj.name)
            if re.match(pattern, api_name):
                return resource_obj
        return None

    @staticmethod
    def _convert_permission(in_method):
        conversion_dict = {'patch': 'update',
                           'put': 'update',
                           'get': 'read',
                           'delete': 'delete',
                           'post': 'create'}
        return conversion_dict.get(in_method.lower())


class APIPermission(BaseComposedPermision):

    def global_permission_set(self):
        return APIPermissionComponent

    def object_permission_set(self):
        return AllowAll
