import django_filters
from .models import Donation

class DonationFilter(django_filters.FilterSet):
    min_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='gte')
    max_amount = django_filters.NumberFilter(field_name="amount", lookup_expr='lte')
    start_date = django_filters.DateFilter(field_name="created_at", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="created_at", lookup_expr='lte')
    payment_method = django_filters.CharFilter(field_name="payment_method", lookup_expr='iexact')
    donation_type = django_filters.CharFilter(field_name="donation_type", lookup_expr='iexact')
    
    class Meta:
        model = Donation
        fields = ['payment_status', 'is_anonymous', 'program']