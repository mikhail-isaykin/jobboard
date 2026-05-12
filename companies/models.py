from django.db import models
from django.conf import settings
from core.utils import validate_image_size
from .utils import logo_upload_path
from django.db.models import Avg


class Company(models.Model):
    owner = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='company',
        verbose_name='Работодатель',
    )
    name = models.CharField(max_length=50, verbose_name='Название компании')
    description = models.TextField(blank=True, verbose_name='Описание')
    website = models.URLField(blank=True, verbose_name='Ссылка на сайт')
    logo = models.ImageField(
        upload_to=logo_upload_path,
        blank=True,
        validators=[validate_image_size],
        verbose_name='Логотип',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Компания'
        verbose_name_plural = 'Компании'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        rating = self.feedbacks.aggregate(avg=Avg('rating'))['avg']
        return round(rating, 1) if rating is not None else 0


class VacancyQuerySet(models.QuerySet):
    '''Только видимые для пользователя вакансии user_vacancies = Vacancy.objects.visible_for_user(request.user)'''
    def visible_for_user(self, user):
        if user.is_authenticated:
            return self.objects.exclude(hidden_vacancies__user=user).exclude(company__hidden_companies__user=user)
        return self


class Vacancy(models.Model):
    objects = VacancyQuerySet.as_manager()
    EMPLOYMENT_CHOICES = [
        ('full_time', 'Полная'),
        ('part_time', 'Частичная'),
        ('internship', 'Стажировка'),
        ('contract', 'Контракт'),
        ('remote', 'Удалённая работа'),
    ]
    SCHEDULE_CHOICES = [
        ('day', 'Дневные смены'),
        ('night', 'Ночные смены'),
        ('flexible', 'Гибкий график'),
        ('shift', 'Сменный график'),
        ('remote', 'Удалённо'),
    ]
    SALARY_TYPE_CHOICES = [
        ('weekly', 'Раз в неделю'),
        ('monthly', 'Раз в месяц'),
        ('twice_monthly', '2 раза в месяц'),
        ('daily', 'Ежедневно'),
        ('hourly', 'По часам'),
        ('negotiable', 'Договорная'),
    ]
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Компания',
    )
    profession = models.ForeignKey(
        'professions.Profession',
        on_delete=models.CASCADE,
        related_name='vacancies',
        verbose_name='Профессия',
    )
    title = models.CharField(max_length=50, verbose_name='Название вакансии')
    description = models.TextField(verbose_name='Общее описание')
    city = models.CharField(max_length=50, verbose_name='Город')
    street = models.CharField(max_length=50, blank=True, verbose_name='Улица')
    salary = models.PositiveIntegerField(null=True, blank=True, verbose_name='Зарплата')
    salary_type = models.CharField(
        max_length=20, choices=SALARY_TYPE_CHOICES, verbose_name='Тип зарплаты'
    )
    experience_from = models.PositiveSmallIntegerField(
        blank=True, null=True, verbose_name='Минимальный опыт'
    )
    employment_type = models.CharField(
        max_length=20,
        choices=EMPLOYMENT_CHOICES,
        default='full_time',
        verbose_name='Тип занятости',
    )
    schedule = models.CharField(
        max_length=20,
        choices=SCHEDULE_CHOICES,
        default='day',
        verbose_name='График работы',
    )
    working_hours = models.CharField(
        max_length=20, blank=True, verbose_name='Рабочие часы'
    )
    responsibilities = models.TextField(blank=True, verbose_name='Обязанности')
    conditions = models.TextField(blank=True, verbose_name='Условия работы')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.title} в {self.company}'


class FeedbackCompany(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Пользователь',
    )
    company = models.ForeignKey(
        'companies.Company',
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Компания',
    )
    vacancy = models.ForeignKey(
        'companies.Vacancy',
        on_delete=models.CASCADE,
        related_name='feedbacks',
        verbose_name='Вакансия',
        default=1
    )
    comment = models.TextField(verbose_name='Отзыв')
    rating = models.PositiveSmallIntegerField(
        choices=[(i, str(i)) for i in range(1, 6)], verbose_name='Рейтинг'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    class Meta:
        verbose_name = 'Отзыв о компании'
        verbose_name_plural = 'Отзывы о компаниях'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'company'], name='unique_feedback_per_user_company'
            )
        ]

    def __str__(self):
        return f'Отзыв о {self.company} — {self.rating}/5'


class FavoriteVacancy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='favorite_vacancies',
        verbose_name='Пользователь',
    )
    vacancy = models.ForeignKey(
        'Vacancy',
        on_delete=models.CASCADE,
        related_name='in_favorites',
        verbose_name='Вакансия',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')

    class Meta:
        verbose_name = 'Избранная вакансия'
        verbose_name_plural = 'Избранные вакансии'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'vacancy'], name='unique_favorite_vacancy_per_user'
            )
        ]

    def __str__(self):
        return f'{self.user} добавил в избранное {self.vacancy}'


class HiddenVacancy(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hidden_vacancies',
        verbose_name='Пользователь',
    )
    vacancy = models.ForeignKey(
        'Vacancy',
        on_delete=models.CASCADE,
        related_name='hidden_vacancies',
        verbose_name='Вакансия',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Скрыто')

    class Meta:
        verbose_name = 'Скрытая вакансия'
        verbose_name_plural = 'Скрытые вакансии'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'vacancy'], name='unique_hidden_vacancy_per_user'
            )
        ]

    def __str__(self):
        return f'{self.user} скрыл {self.vacancy}'


class HiddenCompany(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='hidden_companies',
        verbose_name='Пользователь',
    )
    company = models.ForeignKey(
        'Company',
        on_delete=models.CASCADE,
        related_name='hidden_companies',
        verbose_name='Компания',
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Скрыто')

    class Meta:
        verbose_name = 'Скрытая компания'
        verbose_name_plural = 'Скрытые компании'
        ordering = ['-created_at']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'company'], name='unique_hidden_company_per_user'
            )
        ]

    def __str__(self):
        return f'{self.user} скрыл {self.company}'