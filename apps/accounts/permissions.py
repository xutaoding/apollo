# -*- coding: utf-8 -*-

from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
        自定义权限，只允许对象的所有者编辑它
    """
    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        print 'accounts permission:', request, obj, type(obj)
        return request.user == obj.owner



