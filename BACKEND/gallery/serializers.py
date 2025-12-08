from rest_framework import serializers
from .models import GalleryCategory, GalleryItem, GalleryAlbum

class GalleryCategorySerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(source='items.count', read_only=True)
    
    class Meta:
        model = GalleryCategory
        fields = ['id', 'name', 'slug', 'description', 'item_count', 'created_at']
        read_only_fields = ['slug', 'created_at']

class GalleryItemSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    thumbnail_url = serializers.SerializerMethodField()
    
    class Meta:
        model = GalleryItem
        fields = ['id', 'category', 'category_name', 'title', 'description',
                  'item_type', 'image', 'video_url', 'video_file',
                  'photographer', 'date_taken', 'location', 'is_featured',
                  'is_published', 'thumbnail_url', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']
    
    def get_thumbnail_url(self, obj):
        request = self.context.get('request')
        if obj.thumbnail_url and request:
            return request.build_absolute_uri(obj.thumbnail_url)
        return obj.thumbnail_url

class GalleryAlbumSerializer(serializers.ModelSerializer):
    item_count = serializers.IntegerField(read_only=True)
    items = GalleryItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = GalleryAlbum
        fields = ['id', 'title', 'slug', 'description', 'cover_image',
                  'items', 'item_count', 'is_published', 'created_at', 'updated_at']
        read_only_fields = ['slug', 'created_at', 'updated_at']

class GallerySummarySerializer(serializers.Serializer):
    total_items = serializers.IntegerField()
    total_categories = serializers.IntegerField()
    total_albums = serializers.IntegerField()
    featured_items = GalleryItemSerializer(many=True)
    recent_items = GalleryItemSerializer(many=True)