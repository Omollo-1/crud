from django.db import models
from donations.models import Donation


class MpesaPayment(models.Model):
    """
    Model to track M-Pesa STK Push payments
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Transaction identifiers from M-Pesa
    merchant_request_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    checkout_request_id = models.CharField(max_length=100, unique=True, db_index=True)
    
    # Payment details
    phone_number = models.CharField(max_length=15, help_text="Format: 254XXXXXXXXX")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account_reference = models.CharField(max_length=100, default="Donation")
    transaction_desc = models.CharField(max_length=100, default="Charitize Donation")
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    result_code = models.CharField(max_length=10, null=True, blank=True)
    result_desc = models.TextField(null=True, blank=True)
    
    # M-Pesa transaction details (populated after callback)
    mpesa_receipt_number = models.CharField(max_length=50, null=True, blank=True)
    transaction_date = models.DateTimeField(null=True, blank=True)
    
    # Link to donation
    donation = models.OneToOneField(
        Donation, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='mpesa_payment'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "M-Pesa Payment"
        verbose_name_plural = "M-Pesa Payments"
    
    def __str__(self):
        return f"{self.phone_number} - KES {self.amount} ({self.status})"
    
    def is_successful(self):
        """Check if payment was successful"""
        return self.status == 'completed' and self.result_code == '0'
