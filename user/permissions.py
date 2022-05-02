from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        is_author = False
        is_follower = False
        if request.user.is_authenticated:
            is_author = request.user.role == 'AUTHOR'
            is_follower = request.user.role == 'FOLLOWER'

        if view.action == 'list':
            return True
        elif view.action in ['retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_superuser or is_author
        else:
            return False

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            if obj.type == "PUBLIC":
                return True
            else:
                return request.user.is_authenticated

        elif view.action in ['update', 'partial_update']:
            return request.user.role == "AUTHOR" or request.user.is_superuser
        elif view.action == 'destroy':
            return request.user.role == "AUTHOR" or request.user.is_superuser
        else:
            return False