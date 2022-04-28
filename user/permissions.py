from rest_framework import permissions


class IsFollower(permissions.BasePermission):
    message = 'You must follower.'

    def has_permission(self, request, view):
        if request.user.role == 'Follower':
            return True
        else:
            return False


# class IsAuthor(permissions.BasePermission):
#     message = 'You are not the author.'
#
#     def has_permission(self, request, view):
