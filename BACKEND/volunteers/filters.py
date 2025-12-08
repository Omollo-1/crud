import django_filters
from .models import Volunteer

class VolunteerFilter(django_filters.FilterSet):
    min_age = django_filters.NumberFilter(field_name="age", lookup_expr='gte')
    max_age = django_filters.NumberFilter(field_name="age", lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name="application_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="application_date", lookup_expr='lte')
    commitment_level = django_filters.CharFilter(field_name="commitment_level", lookup_expr='iexact')
    has_background_check = django_filters.BooleanFilter(field_name="has_background_check")
    
    class Meta:
        model = Volunteer
        fields = ['status', 'preferred_time']