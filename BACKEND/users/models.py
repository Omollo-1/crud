from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('donor', 'Donor'),
        ('volunteer', 'Volunteer'),
    ]
    
    phone = models.CharField(max_length=20, blank=True, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='donor')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.username} ({self.role})"
    
    class Meta:
        ordering = ['-date_joined']
        verbose_name = "User"
        verbose_name_plural = "Users"

class Membership(models.Model):
    MEMBERSHIP_TYPES = [
        ('regular', 'Regular'),
        ('premium', 'Premium'),
        ('lifetime', 'Lifetime'),
    ]
    
    full_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    membership_type = models.CharField(max_length=20, choices=MEMBERSHIP_TYPES, default='regular')
    reason_for_joining = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} - {self.membership_type}"