from django.db import models
from django.core.validators import MinValueValidator

class Donation(models.Model):
    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('mpesa', 'M-Pesa'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    
    DONATION_TYPES = [
        ('one_time', 'One-time'),
        ('monthly', 'Monthly'),
        ('annual', 'Annual'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    donor_name = models.CharField(max_length=200)
    donor_email = models.EmailField()
    donor_phone = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    payment_method = models.CharField(max_length=50, choices=PAYMENT_METHODS, default='credit_card')
    donation_type = models.CharField(max_length=20, choices=DONATION_TYPES, default='one_time')
    is_anonymous = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.donor_name} - ${self.amount} ({self.status})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Donation"
        verbose_name_plural = "Donations"


class Donor(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    total_donated = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    donation_count = models.IntegerField(default=0)
    first_donation_date = models.DateTimeField(null=True, blank=True)
    last_donation_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (${self.total_donated})"
    
    class Meta:
        ordering = ['-total_donated']
        verbose_name = "Donor"
        verbose_name_plural = "Donors"


class Campaign(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    goal_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='campaigns/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    def progress_percentage(self):
        if self.goal_amount > 0:
            return (self.current_amount / self.goal_amount) * 100
        return 0
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Campaign"
        verbose_name_plural = "Campaigns"