from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator


class Resume(models.Model):
    GENDER_CHOICES = [
        ('male', 'Мужчина'),
        ('female', 'Женщина'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='resumes',
        verbose_name='Пользователь'
    )
    profession = models.ForeignKey(
        'professions.Profession',
        on_delete=models.PROTECT,
        related_name='resumes',
        verbose_name='Профессия'
    )
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    middle_name = models.CharField(max_length=50, blank=True, verbose_name='Отчество')
    gender = models.CharField(
        max_length=20,
        choices=GENDER_CHOICES,
        blank=True,
        verbose_name='Пол'
    )
    phone = models.CharField(max_length=20, unique=True, verbose_name='Номер телефона')
    date_of_birth = models.DateField(verbose_name='Дата рождения')
    desired_salary = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        verbose_name='Желаемая зарплата'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Резюме'
        verbose_name_plural = 'Резюме'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class ResumeView(models.Model):
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='resume_views',
        verbose_name='Компания'
    )
    resume = models.ForeignKey(
        'Resume',
        on_delete=models.CASCADE,
        related_name='resume_views',
        verbose_name='Резюме'
    )
    date = models.DateField(auto_now_add=True, verbose_name='Дата просмотра')

    class Meta:
        verbose_name = 'Просмотр резюме'
        verbose_name_plural = 'Просмотры резюме'
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'resume', 'date'],
                name='unique_resume_view_per_date'
            )
        ]
    
    def __str__(self):
        return f'{self.company.name} посмотрел {self.resume} ({self.date})'
