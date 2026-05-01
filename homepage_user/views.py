from django.shortcuts import render
from django.views.generic import TemplateView
from core.models import SiteSettings
from communications.models import Response, Invitation
from companies.models import Vacancy

class HomePageView(TemplateView):
    template_name = 'homepage_user/homepage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = SiteSettings.objects.first()
        context['logo'] = obj.logo
        context['main_banner'] = obj.main_banner
        context['total_responses'] = Response.objects.count()
        context['total_invitations'] = Invitation.objects.count()
        context['vacancies'] = Vacancy.objects.select_related('company', 'profession')[:7]
        return context
