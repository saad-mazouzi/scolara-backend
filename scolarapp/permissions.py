from rest_framework import permissions
from rest_framework.permissions import BasePermission

from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

class IsAdmin(permissions.BasePermission):
    """
    Permission pour les admins.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role is not None and request.user.role.name == 'ADMIN'


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Permission pour les admins ou accès en lecture seule pour les autres.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_authenticated:
            # Vérifie si l'utilisateur a un rôle et s'il est admin
            return request.user.role is not None and request.user.role.name == 'ADMIN'
        
        return False


class IsOwner(permissions.BasePermission):
    """
    Permission pour permettre à l'utilisateur propriétaire d'accéder à son propre profil.
    """
    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id
