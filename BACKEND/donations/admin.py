from django.contrib import admin
from django.utils.html import format_html
from .models import Donation, Donor, Campaign

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ('donor_name', 'amount', 'payment_method', 'status', 'created_at', 'action_buttons')
    list_filter = ('status', 'payment_method', 'donation_type', 'created_at')
    search_fields = ('donor_name', 'donor_email', 'donor_phone')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'
    list_per_page = 20
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'payment_method', 'donation_type', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('wide',)
        }),
    )
    
    def action_buttons(self, obj):
        if obj.status == 'pending':
            return format_html(
                '<a class="button" href="#" style="background-color: #4CAF50; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Approve</a> '
                '<a class="button" href="#" style="background-color: #f44336; color: white; padding: 5px 10px; border-radius: 3px; text-decoration: none;">Reject</a>'
            )
        return obj.status
    
    action_buttons.short_description = 'Actions'
    action_buttons.allow_tags = True


@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'total_donated', 'donation_count', 'last_donation_date')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'total_donated', 'donation_count')
    
    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'email', 'phone')
        }),
        ('Donation Statistics', {
            'fields': ('total_donated', 'donation_count', 'first_donation_date', 'last_donation_date')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('title', 'goal_amount', 'current_amount', 'progress_bar', 'is_active', 'created_at')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'progress_display')
    list_per_page = 20
    
    fieldsets = (
        ('Campaign Information', {
            'fields': ('title', 'description', 'image')
        }),
        ('Financial Goals', {
            'fields': ('goal_amount', 'current_amount')
        }),
        ('Timeline', {
            'fields': ('start_date', 'end_date', 'is_active')
        }),
        ('Progress', {
            'fields': ('progress_display',),
            'classes': ('wide',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    def progress_bar(self, obj):
        progress = obj.progress_percentage()
        color = '#4CAF50' if progress >= 75 else '#FFC107' if progress >= 50 else '#F44336'
        return format_html(
            '<div style="width: 100px; background-color: #e0e0e0; border-radius: 3px;">'
            '<div style="width: {}%; height: 20px; background-color: {}; border-radius: 3px; text-align: center; color: white; line-height: 20px;">{}%</div>'
            '</div>',
            progress, color, int(progress)
        )
    
    progress_bar.short_description = 'Progress'
    
    def progress_display(self, obj):
        progress = obj.progress_percentage()
        return f"{progress:.1f}% ({obj.current_amount}/{obj.goal_amount})"
    
    progress_display.short_description = 'Current Progress'