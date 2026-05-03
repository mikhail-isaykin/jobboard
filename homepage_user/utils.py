from django.db.models import Q


def filtered_objects_with_filter_type(queryset, filter_type=None):
    if filter_type == 'part_time':
        queryset = queryset.filter(employment_type='part_time')
    elif filter_type == 'without_experience':
        queryset = queryset.filter(Q(experience_from__isnull=True) | Q(experience_from=0))
    elif filter_type == 'internship':
        queryset = queryset.filter(employment_type='internship')
    elif filter_type == 'remote':
        queryset = queryset.filter(schedule='remote')
    return queryset
