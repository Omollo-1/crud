from django.contrib import admin
from django.utils.html import format_html
from .models import GalleryCategory, GalleryItem, GalleryAlbum

@admin.register(GalleryCategory)
class GalleryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_type', 'category', 'thumbnail_preview', 'is_featured', 'is_published')
    list_filter = ('item_type', 'category', 'is_featured', 'is_published')
    search_fields = ('title', 'description')
    
    def thumbnail_preview(self, obj):
        url = obj.thumbnail_url
        if url:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', url)
        return "No Preview"
    thumbnail_preview.short_description = 'Preview'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(GalleryAlbum)
class GalleryAlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'item_count', 'is_published', 'created_at')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('items',)

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
