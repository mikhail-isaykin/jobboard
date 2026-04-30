from django.db import models
from django.utils import timezone


class Response(models.Model):
    """Отклик на вакансию"""
    vacancy = models.ForeignKey(
        "companies.Vacancy",
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name="Вакансия"
    )
    resume = models.ForeignKey(
        "resumes.Resume",
        on_delete=models.CASCADE,
        related_name="responses",
        verbose_name="Резюме"
    )
    cover_letter = models.TextField(
        blank=True,
        null=True,
        verbose_name="Сопроводительное письмо"
    )
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Дата отклика")
    status = models.CharField(
        max_length=20,
        choices=[
            ("new", "Новый"),
            ("viewed", "Просмотрен"),
            ("accepted", "Принят"),
            ("rejected", "Отклонён"),
        ],
        default="new",
        verbose_name="Статус"
    )
