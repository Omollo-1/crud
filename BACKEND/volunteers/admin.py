from django.contrib import admin
from django.utils.html import format_html
from .models import Volunteer, VolunteerAssignment

@admin.register(Volunteer)
class VolunteerAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'status', 'application_date', 'action_buttons')
    list_filter = ('status', 'commitment_level', 'application_date')
    search_fields = ('name', 'email', 'phone', 'skills')
    readonly_fields = ('application_date', 'created_at', 'updated_at')
    actions = ['approve_volunteer', 'reject_volunteer']

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone', 'age', 'occupation', 'address')
        }),
        ('Skills & Commitment', {
            'fields': ('skills', 'interests', 'availability', 'preferred_time', 'commitment_level')
        }),
        ('Application Details', {
            'fields': ('motivation', 'emergency_contact_name', 'emergency_contact_phone', 'emergency_contact_relation')
        }),
        ('Status & Notes', {
            'fields': ('status', 'start_date', 'end_date', 'has_background_check', 'background_check_date', 'notes')
        }),
        ('Metadata', {
            'fields': ('application_date', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="#" style="background-color: #2a9d8f; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Approve</a> '
                '<a class="button" href="#" style="background-color: #e63946; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none; margin-left: 5px;">Reject</a>'
            )
        return obj.get_status_display()
    action_buttons.short_description = 'Quick Actions'

    def approve_volunteer(self, request, queryset):
        queryset.update(status='approved')
    approve_volunteer.short_description = "Approve selected volunteers"

    def reject_volunteer(self, request, queryset):
        queryset.update(status='rejected')
    reject_volunteer.short_description = "Reject selected volunteers"

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }

@admin.register(VolunteerAssignment)
class VolunteerAssignmentAdmin(admin.ModelAdmin):
    list_display = ('volunteer', 'program', 'role', 'start_date', 'is_active')
    list_filter = ('is_active', 'start_date')
    search_fields = ('volunteer__name', 'program__title', 'role')
