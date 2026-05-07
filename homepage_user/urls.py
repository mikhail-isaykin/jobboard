from django.urls import path
from .views import HomePageView


app_name = 'homepage_user'

urlpatterns = [
    path('', HomePageView.as_view(), name='homepage'),
]
