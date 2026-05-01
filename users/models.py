from django.db import models
from django.conf import settings
from core.utils import validate_image_size
from .utils import avatar_upload_path


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    avatar = models.ImageField(
        upload_to=avatar_upload_path,
        blank=True,
        validators=[validate_image_size],
        verbose_name='Аватар'
    )
    bio = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон'
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name='Дата рождения'
    )
    location = models.CharField(
        max_length=50,
        blank=True,
        verbose_name='Город'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Верифицирован'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Создан'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Обновлен'
    )

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        ordering = ['-updated_at']

    def __str__(self):
        return self.user.username
