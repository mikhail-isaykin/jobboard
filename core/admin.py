from django.contrib import admin
from .models import SiteSettings


@admin.register(SiteSettings)
class SiteSettings(admin.ModelAdmin)
    list_display = ('logo', 'main_banner')
