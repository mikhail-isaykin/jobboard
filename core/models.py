from django.db import models
from .utils import validate_image_size


class SiteSettings(models.Model):
    logo = models.ImageField(
        validators=[validate_image_size], verbose_name='Логотип сайта'
    )
    main_banner = models.ImageField(
        validators=[validate_image_size], verbose_name='Hero изображение'
    )

    class Meta:
        verbose_name = 'Настройки сайта'
        verbose_name_plural = 'Настройки сайта'

    def __str__(self):
        return 'Настройки сайта'
