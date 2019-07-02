from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAuthenticatedAndVerified(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_verified()


class IsPublisher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_publisher() and request.user.is_verified())
        return False


class IsSearcher(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_searcher() and request.user.is_verified())
        return False

class HasTradingDoc(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return (request.user.is_publisher() and request.user.has_trading_doc())
        return False

