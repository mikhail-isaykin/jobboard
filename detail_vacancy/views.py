from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from core.models import SiteSettings
from companies.models import Vacancy, FeedbackCompany, HiddenVacancy, Complaint
from .utils import render_stars_html, years_declension, split_lines
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render
from django.contrib import messages
from django.shortcuts import redirect
from companies.forms import ComplaintForm


class DetailVacancyView(LoginRequiredMixin, DetailView):
    model = Vacancy
    template_name = 'detail_vacancy/detail_vacancy.html'
    context_object_name = 'vacancy'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['logo'] = obj.logo if (obj := SiteSettings.objects.first()) else None
        context['user_city'] = self.request.user.profile.location if hasattr(self.request.user, 'profile') else 'Москва'
        unhidden_vacancies = Vacancy.objects.visible_for_user(self.request.user)
        context['vacancies_company'] = unhidden_vacancies.filter(company=self.object.company).exclude(pk=self.object.pk)
        context['similar_vacancies'] = unhidden_vacancies.exclude(company=self.object.company)[:2]
        context['feedbacks_company'] = FeedbackCompany.objects.filter(company=self.object.company)[:4]
        rating = self.object.company.average_rating
        context['rating'] = rating
        context['stars_rating'] = render_stars_html(rating)
        context['experience_required'] = years_declension(self.object.experience_from)
        context['responsibilities'] = split_lines(self.object.responsibilities)
        context['conditions'] = split_lines(self.object.conditions)
        return context

@login_required
def hide_vacancy(request, pk):
    if request.method == 'POST':
        vacancy = get_object_or_404(Vacancy, pk=pk)
        HiddenVacancy.objects.get_or_create(user=request.user, vacancy=vacancy)
        messages.success(request, 'Вакансия скрыта')
    return redirect('homepage_user:homepage')


@login_required
def submit_complaint(request):
    form = ComplaintForm()
    if request.method == 'POST':
        vacancy_id = request.POST.get('vacancy_id')
        vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.vacancy = vacancy
            complaint.save()
            messages.success(request, 'Ваша жалоба успешно отправлена!')
            return redirect('vacancy_detail')
    vacancy_id = request.GET.get('vacancy_id')
    return render(request, 'complaint.html', {'form': form, 'vacancy_id': vacancy_id})
