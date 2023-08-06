class UzcloudBillingAccountMixin:
    def is_group_member(self, group_name: str) -> bool:
        return self.user.groups.filter(name=group_name).exists()
