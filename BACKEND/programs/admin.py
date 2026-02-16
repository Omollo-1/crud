from django.contrib import admin
from django.utils.html import format_html
from .models import Program, ProgramUpdate, ProgramBeneficiary

class ProgramUpdateInline(admin.TabularInline):
    model = ProgramUpdate
    extra = 1

class ProgramBeneficiaryInline(admin.TabularInline):
    model = ProgramBeneficiary
    extra = 1

@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'progress_bar', 'beneficiaries_count', 'volunteers_needed')
    list_filter = ('category', 'status', 'start_date')
    search_fields = ('title', 'short_description', 'description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProgramUpdateInline, ProgramBeneficiaryInline]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'status', 'short_description', 'description')
        }),
        ('Visuals', {
            'fields': ('image', 'banner_image')
        }),
        ('Timeline & Location', {
            'fields': ('start_date', 'end_date', 'location')
        }),
        ('Impact & Goals', {
            'fields': ('target_amount', 'current_amount', 'beneficiaries_count', 'volunteers_needed')
        }),
        ('Metadata & SEO', {
            'fields': ('features', 'meta_title', 'meta_description', 'published_at'),
            'classes': ('collapse',)
        }),
    )

    def progress_bar(self, obj):
        progress = obj.progress_percentage
        color = '#e63946' if progress < 30 else '#f4a261' if progress < 70 else '#2a9d8f'
        return format_html(
            '<div style="width: 100px; background-color: #f1f1f1; border-radius: 5px; border: 1px solid #ccc;">'
            '<div style="width: {}%; height: 12px; background-color: {}; border-radius: 5px;"></div>'
            '</div>'
            '<span style="font-size: 10px; color: #666;">{}% of target</span>',
            progress, color, int(progress)
        )
    progress_bar.short_description = 'Funding Progress'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(ProgramUpdate)
class ProgramUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'program', 'created_at')
    list_filter = ('program', 'created_at')
    search_fields = ('title', 'content')

@admin.register(ProgramBeneficiary)
class ProgramBeneficiaryAdmin(admin.ModelAdmin):
    list_display = ('name', 'program', 'age', 'joined_date', 'is_active')
    list_filter = ('program', 'is_active', 'joined_date')
    search_fields = ('name', 'story')
