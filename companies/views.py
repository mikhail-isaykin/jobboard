from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from companies.models import Vacancy, FavoriteVacancy, HiddenVacancy


@login_required
def toggle_favorite(request, vacancy_id):
    vacancy = get_object_or_404(Vacancy, pk=vacancy_id)
    favorite_vacancy, created = FavoriteVacancy.objects.get_or_create(
        user=request.user, vacancy=vacancy
    )
    if not created:
        favorite_vacancy.delete()
        return JsonResponse(
            {
                'status': 'removed',
                'favorite_count': FavoriteVacancy.objects.filter(
                    user=request.user
                ).count(),
            }
        )
    return JsonResponse(
        {
            'status': 'added',
            'favorite_count': FavoriteVacancy.objects.filter(user=request.user).count(),
        }
    )


@login_required
@require_POST
def toggle_hidden_vacancy(request):
    vacancy_id = request.POST.get('vacancy_id')
    vacancy = Vacancy.objects.filter(pk=vacancy_id).first()
    if not vacancy:
        return JsonResponse({'status': 'not found'}, status=404)
    hidden_vacancy, created = HiddenVacancy.objects.get_or_create(
        user=request.user, vacancy=vacancy
    )
    if not created:
        hidden_vacancy.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'hidden'})
