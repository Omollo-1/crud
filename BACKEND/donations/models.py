from django.db import models

# Create your models here.
from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from users.models import User

class Donation(models.Model):
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('credit_card', 'Credit Card'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
    )
    
    DONATION_TYPE_CHOICES = (
        ('one_time', 'One Time'),
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    )
    
    donor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    donor_name = models.CharField(max_length=255)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(1)])
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPE_CHOICES, default='one_time')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    dedication = models.TextField(blank=True, null=True)
    program = models.ForeignKey('programs.Program', on_delete=models.SET_NULL, null=True, blank=True, related_name='donations')
    is_anonymous = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = _('Donation')
        verbose_name_plural = _('Donations')
    
    def __str__(self):
        return f"Donation #{self.id} - {self.donor_name} - ${self.amount}"
    
    @property
    def display_amount(self):
        return f"${self.amount} {self.currency}"
    
    def mark_as_completed(self, transaction_id=None):
        self.payment_status = 'completed'
        if transaction_id:
            self.transaction_id = transaction_id
        self.save()
    
    def mark_as_failed(self):
        self.payment_status = 'failed'
        self.save()

class RecurringDonation(models.Model):
    donor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recurring_donations')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    frequency = models.CharField(max_length=20, choices=(
        ('monthly', 'Monthly'),
        ('quarterly', 'Quarterly'),
        ('yearly', 'Yearly'),
    ))
    payment_method = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    next_payment_date = models.DateField()
    last_payment_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Recurring Donation #{self.id} - {self.donor.username}"