from django.urls import path
from .views import toggle_favorite


urlpatterns = [
    path('toggle/<int:vacancy_id>/', toggle_favorite, name='toggle_favorite'),
]
