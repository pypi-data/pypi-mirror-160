from rest_framework.permissions import BasePermission


class IsBillingGroupPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.billing_account.is_group_member(
            group_name="Uzcloud_Billing"
        )
