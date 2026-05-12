from django.urls import path
from .views import toggle_favorite, toggle_hidden_vacancy, hide_company


urlpatterns = [
    path('toggle/<int:vacancy_id>/', toggle_favorite, name='toggle_favorite'),
    path('toggle-hidden-vacancy/', toggle_hidden_vacancy, name='toggle_hidden_vacancy'),
    path('company/hide/<int:pk>/', hide_company, name='hide_company'),
]
