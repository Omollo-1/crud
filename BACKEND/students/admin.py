from django.contrib import admin
from django.utils.html import format_html
from .models import Student, Transcript

class TranscriptInline(admin.TabularInline):
    model = Transcript
    extra = 1

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'student_class', 'age', 'date_joined', 'health_status_preview', 'profile_photo_preview')
    list_filter = ('student_class', 'date_joined', 'programs_enrolled')
    search_fields = ('full_name', 'interests', 'talents', 'core_values')
    filter_horizontal = ('programs_enrolled',)
    inlines = [TranscriptInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('full_name', 'profile_photo', 'date_of_birth', 'date_joined', 'student_class')
        }),
        ('Personal Details', {
            'fields': ('interests', 'talents', 'core_values')
        }),
        ('Health & Programs', {
            'fields': ('health_status', 'programs_enrolled')
        }),
    )

    def profile_photo_preview(self, obj):
        if obj.profile_photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 5px;" />', obj.profile_photo.url)
        return "No Photo"
    profile_photo_preview.short_description = 'Photo'

    def health_status_preview(self, obj):
        if obj.health_status:
            return (obj.health_status[:50] + '...') if len(obj.health_status) > 50 else obj.health_status
        return "N/A"
    health_status_preview.short_description = 'Health Status'

@admin.register(Transcript)
class TranscriptAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'date_uploaded', 'download_link')
    list_filter = ('student', 'date_uploaded')
    search_fields = ('title', 'description', 'student__full_name')

    def download_link(self, obj):
        if obj.file:
            return format_html('<a href="{}" download>Download</a>', obj.file.url)
        return "No File"
    download_link.short_description = 'Download Transcript'
