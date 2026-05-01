from django.contrib import admin
from .models import Response


@admin.register(Response)
class ResponseAdmin(admin.ModelAdmin):
    readonly_fields = ('created_at',)
    list_display = ('vacancy', 'resume', 'status', 'created_at')
    search_fields = ('vacancy__title', 'resume__last_name')
    list_filter = ('status', 'created_at')
