from django.db import models


class Response(models.Model):
    STATUS_CHOICES = [
        ('new', 'Новый'),
        ('viewed', 'Просмотрен'),
        ('accepted', 'Принят'),
        ('rejected', 'Отклонён'),
    ]
    vacancy = models.ForeignKey(
        'companies.Vacancy',
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Вакансия'
    )
    resume = models.ForeignKey(
        'resumes.Resume',
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name='Резюме',
    )
    cover_letter = models.TextField(
        blank=True,
        verbose_name='Сопроводительное письмо'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата отклика'
    )
    status = models.CharField(
        max_length=20,
        default='new',
        choices=STATUS_CHOICES,
        verbose_name='Статус отклика',
    )

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['vacancy', 'resume'],
                name='unique_response_per_vacancy_resume'
            )
        ]

    def __str__(self):
        return (
            f'Отклик на «{self.vacancy}» от {self.resume} ({self.get_status_display()})'
        )
