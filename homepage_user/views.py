from django.views.generic import TemplateView
from core.models import SiteSettings
from communications.models import Response, Invitation
from companies.models import Vacancy, FavoriteVacancy
from django.db.models import Count
from .mixins import NoCompanyRequiredMixin
from resumes.models import ResumeView


class HomePageView(NoCompanyRequiredMixin, TemplateView):
    template_name = 'homepage_user/homepage.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = SiteSettings.objects.first()
        context['logo'] = obj.logo if obj else None
        context['main_banner'] = obj.main_banner if obj else None
        context['total_responses'] = Response.objects.filter(resume__user = self.request.user).count()
        context['total_invitations'] = Invitation.objects.filter(resume__user = self.request.user).count()
        context['resume_views'] = ResumeView.objects.filter(resume__user = self.request.user).count()
        context['favorite_vacancy'] = FavoriteVacancy.objects.filter(user = self.request.user).count()
        context['vacancies'] = Vacancy.objects.select_related('company', 'profession')[:7].annotate(feedback_count=Count('company__feedbacks'))
        context['user_favorites'] = FavoriteVacancy.objects.filter(user=self.request.user).values_list('vacancy_id', flat=True)
        return context
