from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import SiteSettings
from companies.models import Vacancy, FeedbackCompany
from .utils import render_stars_html


class DetailVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'detail_vacancy/detail_vacancy.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = obj.logo if (obj := SiteSettings.objects.first()) else None
        context['user_city'] = self.request.user.profile.location if hasattr(self.request.user, 'profile') else 'Москва'
        context['vacancies_company'] = Vacancy.objects.filter(company=self.object.company).exclude(pk=self.object.pk)
        context['similar_vacancies'] = Vacancy.objects.exclude(company=self.object.company)[:2]
        context['feedbacks_company'] = FeedbackCompany.objects.filter(company=self.object.company)[:4]
        rating = self.object.company.average_rating
        context['rating'] = rating
        context['stars_rating'] = render_stars_html(rating)
        return context
