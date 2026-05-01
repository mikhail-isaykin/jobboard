from django.contrib import admin
from .models import Resume, ResumeView


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Пользователь', {'fields': ('user',)}),
        (
            'Личные данные',
            {
                'fields': (
                    'first_name',
                    'last_name',
                    'middle_name',
                    'gender',
                    'date_of_birth',
                )
            },
        ),
        ('Контакты', {'fields': ('phone',)}),
        ('Работа', {'fields': ('desired_salary',)}),
        ('Даты', {'fields': ('created_at', 'updated_at')}),
    )
    readonly_fields = ('created_at', 'updated_at')
    list_display = (
        'id',
        'user',
        'last_name',
        'first_name',
        'phone',
        'desired_salary',
        'created_at',
    )
    list_filter = ('gender', 'created_at')
    search_fields = ('last_name', 'first_name', 'phone', 'user__username')


class ResumeInline(admin.StackedInline):
    model = Resume
    can_delete = True
    extra = 0


@admin.register(ResumeView)
class ResumeViewAdmin(admin.ModelAdmin):
    readonly_fields = ('date',)
    list_display = ('company', 'resume', 'date')
    list_filter = ('company__name', 'date')
    search_fields = ('company__name', 'resume__last_name')
