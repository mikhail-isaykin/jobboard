from django.urls import path
from .views import DetailVacancyView, hide_vacancy


urlpatterns = [
    path('vacancy/<int:pk>/', DetailVacancyView.as_view(), name='vacancy_detail'),
    path('vacancy/hide/<int:pk>/', hide_vacancy, name='hide_vacancy'),
]
