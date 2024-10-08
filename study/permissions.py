from rest_framework.permissions import BasePermission


class IsStaff(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_staff


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsSuper(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_superuser
