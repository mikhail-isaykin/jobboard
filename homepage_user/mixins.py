from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect


class NoCompanyRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = '/accounts/login/'

    def test_func(self):
        return not hasattr(self.request.user, 'company')

    def handle_no_permission(self):
        return redirect('company')
