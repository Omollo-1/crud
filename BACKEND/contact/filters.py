import django_filters
from .models import ContactMessage

class ContactMessageFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name='submitted_at', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='submitted_at', lookup_expr='lte')
    category = django_filters.CharFilter(field_name='category', lookup_expr='iexact')
    replied = django_filters.BooleanFilter(field_name='replied_at', lookup_expr='isnull', exclude=True)
    
    class Meta:
        model = ContactMessage
        fields = ['status', 'category']