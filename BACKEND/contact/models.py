from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class ContactMessage(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    )
    
    CATEGORY_CHOICES = (
        ('general', 'General Inquiry'),
        ('donation', 'Donation Related'),
        ('volunteer', 'Volunteer Related'),
        ('program', 'Program Related'),
        ('sponsorship', 'Child Sponsorship'),
        ('partnership', 'Partnership'),
        ('other', 'Other'),
    )
    
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)
    subject = models.CharField(max_length=255)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='general')
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    
    # Response tracking
    replied_at = models.DateTimeField(null=True, blank=True)
    reply_message = models.TextField(blank=True, null=True)
    replied_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Metadata
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Timestamps
    submitted_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-submitted_at']
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
    
    def __str__(self):
        return f"{self.name} - {self.subject}"
    
    def mark_as_read(self):
        self.status = 'read'
        self.save()
    
    def reply(self, message, user=None):
        self.status = 'replied'
        self.reply_message = message
        self.replied_at = timezone.now()
        if user:
            self.replied_by = user
        self.save()

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    unsubscribed_at = models.DateTimeField(null=True, blank=True)
    
    # Additional info
    name = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=100, blank=True, null=True)
    
    class Meta:
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email
    
    def unsubscribe(self):
        self.is_active = False
        self.unsubscribed_at = timezone.now()
        self.save()

class SiteConfiguration(models.Model):
    site_name = models.CharField(max_length=100, default='Chartitze')
    contact_email = models.EmailField(default='contact@chartitze.org')
    admin_email = models.EmailField(default='admin@chartitze.org')
    phone_number = models.CharField(max_length=20, default='+254 123 456 789')
    address = models.TextField(default='123 Hope Street, Nairobi, Kenya')
    
    # Social media
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)
    youtube_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)
    
    # Working hours
    working_hours = models.TextField(default='Monday - Friday: 8:00 AM - 6:00 PM\nSaturday: 9:00 AM - 2:00 PM')
    
    # About us
    about_us = models.TextField(blank=True, null=True)
    mission_statement = models.TextField(blank=True, null=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Site Configuration'
        verbose_name_plural = 'Site Configuration'
    
    def __str__(self):
        return 'Site Configuration'
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def load(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj