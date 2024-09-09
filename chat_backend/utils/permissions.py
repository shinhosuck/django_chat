from rest_framework.permissions import BasePermission, IsAdminUser


class CanAccessUserProfiles(IsAdminUser):

    message = 'You are not authorized to access this site!'

    # def has_permission(self, request, view):
    #     is_staff = request.user.is_staff
    #     return is_staff

class IsActiveUser(BasePermission):

    message = 'You account has been disabled'

    def has_permission(self, request, view):
        user = request.user
        user.is_active = True
        is_active = user.is_active
        return is_active