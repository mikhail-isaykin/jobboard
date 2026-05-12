from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied


class NoCompanyRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login/'

    def test_func(self):
        return not hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return redirect('homepage_user:homepage')