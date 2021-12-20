from rest_framework import permissions


class PublicacionPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        elif view.action == 'create':
            return request.user.is_authenticated
        elif view.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        # if not request.user.is_authenticated:
        #     return False
        if view.action == 'retrieve':
            return obj
        elif view.action in ['update', 'partial_update', 'destroy']:
            return obj.autor == request.user
        else:
            return False
