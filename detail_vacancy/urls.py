from django.urls import path
from .views import DetailVacancyView


urlpatterns = [
    path('vacancy/<int:pk>/', DetailVacancyView.as_view(), name='vacancy_detail'),
]
