from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from companies.models import Vacancy, FavoriteVacancy


@login_required
def toggle_favorite(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    favorite_vacancy, created = FavoriteVacancy.objects.get_or_create(user=request.user, vacancy=vacancy)
    if not created:
        favorite_vacancy.delete()
        return JsonResponse({
            'status': 'removed',
            'favorite_count': FavoriteVacancy.objects.filter(user=request.user).count()
        })
    return JsonResponse({
        'status': 'added',
        'favorite_count': FavoriteVacancy.objects.filter(user=request.user).count()
    })
