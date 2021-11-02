from rest_framework.permissions import BasePermission, SAFE_METHODS

from dashboard_app.models import User


class IsAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user == User.objects.get(pk=view.request.user.id)

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
