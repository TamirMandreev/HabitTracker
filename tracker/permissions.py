from rest_framework import permissions


class IsUser(permissions.BasePermission):
    ''' Проверяет, принадлежит ли пользователю привычка '''

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False