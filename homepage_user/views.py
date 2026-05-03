from django.views.generic import TemplateView
from core.models import SiteSettings
from communications.models import Response, Invitation
from companies.models import Vacancy, FavoriteVacancy
from django.db.models import Count
from .mixins import NoCompanyRequiredMixin
from resumes.models import ResumeView
from .utils import filtered_objects_with_filter_type
from users.models import Profile


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
        vacancies = (Vacancy.objects.all()
            .select_related('company', 'profession')
            .annotate(feedback_count=Count('company__feedbacks'))
            .exclude(hidden_vacancies__user=self.request.user))
        vacancies = filtered_objects_with_filter_type(vacancies, self.request.GET.get('filter'))
        context['vacancies'] = vacancies[:7]
        context['user_favorites'] = FavoriteVacancy.objects.filter(user=self.request.user).values_list('vacancy_id', flat=True)
        return context
