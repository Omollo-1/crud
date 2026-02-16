from django.contrib import admin
from django.utils.html import format_html
from .models import MpesaPayment

@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'amount', 'colored_status', 'mpesa_receipt_number', 'checkout_request_id', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['phone_number', 'mpesa_receipt_number', 'checkout_request_id', 'merchant_request_id']
    readonly_fields = ['merchant_request_id', 'checkout_request_id', 'result_code', 'result_desc', 
                      'mpesa_receipt_number', 'transaction_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('phone_number', 'amount', 'account_reference', 'transaction_desc', 'donation')
        }),
        ('M-Pesa Transaction Credentials', {
            'fields': ('merchant_request_id', 'checkout_request_id', 'mpesa_receipt_number', 'transaction_date')
        }),
        ('Status info', {
            'fields': ('status', 'result_code', 'result_desc')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def colored_status(self, obj):
        colors = {
            'completed': '#2a9d8f',
            'pending': '#f4a261',
            'failed': '#e63946',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; border-radius: 10px; font-weight: bold;">{}</span>',
            color, obj.status.upper()
        )
    colored_status.short_description = 'Status'

    class Media:
        css = {
            'all': ('admin/css/custom_admin.css',)
        }
    
    def has_add_permission(self, request):
        return False
