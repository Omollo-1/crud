from django.contrib import admin
from .models import MpesaPayment


@admin.register(MpesaPayment)
class MpesaPaymentAdmin(admin.ModelAdmin):
    list_display = ['phone_number', 'amount', 'status', 'mpesa_receipt_number', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['phone_number', 'mpesa_receipt_number', 'checkout_request_id', 'merchant_request_id']
    readonly_fields = ['merchant_request_id', 'checkout_request_id', 'result_code', 'result_desc', 
                      'mpesa_receipt_number', 'transaction_date', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Payment Details', {
            'fields': ('phone_number', 'amount', 'account_reference', 'transaction_desc', 'donation')
        }),
        ('M-Pesa Transaction Info', {
            'fields': ('merchant_request_id', 'checkout_request_id', 'mpesa_receipt_number', 'transaction_date')
        }),
        ('Status', {
            'fields': ('status', 'result_code', 'result_desc')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Prevent manual creation of payments through admin
        return False
