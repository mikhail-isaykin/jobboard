from django.urls import path
from .views import DetailVacancyView, hide_vacancy, submit_complaint


urlpatterns = [
    path('vacancy/<int:pk>/', DetailVacancyView.as_view(), name='vacancy_detail'),
    path('vacancy/hide/<int:pk>/', hide_vacancy, name='hide_vacancy'),
    path('vacancy/<int:vacancy_id>/complaint/', submit_complaint, name='submit_complaint'),
]
