from django.db import models

# Create your models here.
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class Volunteer(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )
    
    AVAILABILITY_CHOICES = (
        ('weekdays', 'Weekdays'),
        ('weekends', 'Weekends'),
        ('both', 'Both Weekdays and Weekends'),
        ('flexible', 'Flexible'),
    )
    
    TIME_CHOICES = (
        ('mornings', 'Mornings'),
        ('afternoons', 'Afternoons'),
        ('evenings', 'Evenings'),
        ('anytime', 'Anytime'),
    )
    
    COMMITMENT_CHOICES = (
        ('occasional', 'Occasional'),
        ('weekly', 'Weekly (2-4 hours)'),
        ('regular', 'Regular (5+ hours)'),
        ('full_time', 'Full-time (seasonal)'),
    )
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='volunteer_profile', null=True, blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    age = models.PositiveIntegerField()
    occupation = models.CharField(max_length=255, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    
    # Skills and interests
    skills = models.TextField(help_text="List your relevant skills and experience")
    interests = models.JSONField(default=list, help_text="Selected volunteer interests")
    
    # Availability
    availability = models.JSONField(default=list, help_text="Selected availability options")
    preferred_time = models.CharField(max_length=20, choices=TIME_CHOICES, default='anytime')
    commitment_level = models.CharField(max_length=20, choices=COMMITMENT_CHOICES)
    
    # Application details
    motivation = models.TextField(help_text="Why do you want to volunteer with us?")
    emergency_contact_name = models.CharField(max_length=255, blank=True, null=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True, null=True)
    emergency_contact_relation = models.CharField(max_length=100, blank=True, null=True)
    
    # Status and tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    application_date = models.DateField(auto_now_add=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    
    # Additional information
    has_background_check = models.BooleanField(default=False)
    background_check_date = models.DateField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-application_date']
        verbose_name = _('Volunteer')
        verbose_name_plural = _('Volunteers')
    
    def __str__(self):
        return f"{self.name} - {self.get_status_display()}"
    
    @property
    def is_active(self):
        return self.status in ['approved', 'active']
    
    def approve(self):
        self.status = 'approved'
        self.save()
    
    def reject(self):
        self.status = 'rejected'
        self.save()
    
    def activate(self):
        self.status = 'active'
        if not self.start_date:
            self.start_date = timezone.now().date()
        self.save()
    
    def deactivate(self):
        self.status = 'inactive'
        self.end_date = timezone.now().date()
        self.save()

class VolunteerAssignment(models.Model):
    volunteer = models.ForeignKey(Volunteer, on_delete=models.CASCADE, related_name='assignments')
    program = models.ForeignKey('programs.Program', on_delete=models.CASCADE, related_name='volunteer_assignments')
    role = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    hours_per_week = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.volunteer.name} - {self.program.title}"