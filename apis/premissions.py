# permissions.py
from rest_framework import permissions

class SuperUserOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser

class onlyUnAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
    
class SuperOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser or (request.method in permissions.SAFE_METHODS)
