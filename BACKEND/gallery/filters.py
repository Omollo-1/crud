import django_filters
from .models import GalleryItem

class GalleryItemFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(field_name='category__slug')
    item_type = django_filters.CharFilter(field_name='item_type', lookup_expr='iexact')
    is_featured = django_filters.BooleanFilter(field_name='is_featured')
    start_date = django_filters.DateFilter(field_name='date_taken', lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name='date_taken', lookup_expr='lte')
    
    class Meta:
        model = GalleryItem
        fields = ['category', 'item_type', 'is_featured']