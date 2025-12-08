import django_filters
from .models import Program

class ProgramFilter(django_filters.FilterSet):
    min_target_amount = django_filters.NumberFilter(field_name="target_amount", lookup_expr='gte')
    max_target_amount = django_filters.NumberFilter(field_name="target_amount", lookup_expr='lte')
    min_beneficiaries = django_filters.NumberFilter(field_name="beneficiaries_count", lookup_expr='gte')
    start_date = django_filters.DateFilter(field_name="start_date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="end_date", lookup_expr='lte')
    
    class Meta:
        model = Program
        fields = ['category', 'status', 'location']