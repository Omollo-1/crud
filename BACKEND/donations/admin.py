from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.utils.html import format_html
from .models import Donation, RecurringDonation

@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor_name', 'amount_display', 'payment_status', 
                    'payment_method', 'created_at', 'is_anonymous']
    list_filter = ['payment_status', 'payment_method', 'donation_type', 
                   'is_anonymous', 'created_at']
    search_fields = ['donor_name', 'donor_email', 'transaction_id']
    readonly_fields = ['created_at', 'updated_at']
    actions = ['mark_as_completed', 'mark_as_failed']
    
    fieldsets = (
        ('Donor Information', {
            'fields': ('donor', 'donor_name', 'donor_email', 'donor_phone', 'is_anonymous')
        }),
        ('Donation Details', {
            'fields': ('amount', 'currency', 'donation_type', 'program', 'dedication')
        }),
        ('Payment Information', {
            'fields': ('payment_method', 'payment_status', 'transaction_id', 'notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    
    def amount_display(self, obj):
        return obj.display_amount
    amount_display.short_description = 'Amount'
    
    def mark_as_completed(self, request, queryset):
        queryset.update(payment_status='completed')
        self.message_user(request, f"{queryset.count()} donations marked as completed.")
    mark_as_completed.short_description = "Mark selected donations as completed"
    
    def mark_as_failed(self, request, queryset):
        queryset.update(payment_status='failed')
        self.message_user(request, f"{queryset.count()} donations marked as failed.")
    mark_as_failed.short_description = "Mark selected donations as failed"

@admin.register(RecurringDonation)
class RecurringDonationAdmin(admin.ModelAdmin):
    list_display = ['id', 'donor', 'amount', 'frequency', 'is_active', 
                    'next_payment_date', 'last_payment_date']
    list_filter = ['frequency', 'is_active', 'created_at']
    search_fields = ['donor__username', 'donor__email']