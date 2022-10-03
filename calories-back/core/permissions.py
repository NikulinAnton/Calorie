from rest_framework.permissions import IsAuthenticated


class IsSuperuser(IsAuthenticated):
    def has_permission(self, request, view):
        if not super().has_permission(request, view):
            return False
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser


class IsObjectOwner(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.user == obj.owner


IsSuperuserOrIsObjectOwner = IsSuperuser | IsObjectOwner